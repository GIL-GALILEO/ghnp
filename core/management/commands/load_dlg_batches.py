import os
import logging
import subprocess
from datetime import datetime
import time
from optparse import make_option
from shutil import copyfile

from solr import SolrConnection

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from chronam.core.batch_loader import BatchLoader
from chronam.core import batch_loader
from chronam.core.management.commands import configure_logging
from chronam.core import title_loader
from chronam.core.index import index_titles
from chronam.core.models import Title

from slackclient import SlackClient

configure_logging('load_dlg_batches_logging.config',
                  'load_dlg_batches_%s.log' % os.getpid())

_logger = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip-process-ocr',
                    action='store_false',
                    dest='process_ocr', default=True,
                    help='Do not generate ocr, and index'),
        make_option('--skip-process-coordinates',
                    action='store_false',
                    dest='process_coordinates', default=True,
                    help='Do not write out word coordinates'),
    )
    help = "Load batches by name from a batch list file"
    args = '<batch_list_filename>'

    def handle(self, *args, **options):

        def get_immediate_subdirectories(a_dir):
            return [name for name in os.listdir(a_dir)
                    if os.path.isdir(os.path.join(a_dir, name))]

        def slack(message):
            sc.api_call("chat.postMessage", channel="#ghnp", text=message)

        start = datetime.now()

        sc = SlackClient(settings.SLACK_KEY)

        loader = BatchLoader()

        new_batches_location = '/opt/chronam/data/chronamftp/new_batches/'
        replacement_batches_location = '/opt/chronam/data/chronamftp/replacement_batches/'
        nonlccn_location = '/opt/chronam/data/nonlccn/'
        batch_drop = '/opt/chronam/data/dlg_batches/drop/'

        # GET LIST OF BATCHES TO LOAD
        new_batches = get_immediate_subdirectories(new_batches_location)
        replacement_batches = get_immediate_subdirectories(replacement_batches_location)

        # CHECK new_batches FOR finalMARC FOLDERS
        new_title_folders = []
        for folder in new_batches:
            if 'MARC' in folder:
                new_title_folders.append(folder)
                new_batches.remove(folder)

        # ISSUE STARTING NOTIFICATIONS
        slack('Starting DLG Batch Load Process! Found `%s` new batches and `%s` replacement batches available to load.' % (len(new_batches), len(replacement_batches)))

        # RUN KEVIN'S RSYNC COMMANDS, WAIT
        slack('RSync of batches is starting')
        start_time = time.time()
        slack('Copying new batches')
        subprocess.call(['rsync -rav --progress /opt/chronam/data/chronamftp/new_batches/* /opt/chronam/data/dlg_batches/drop/'])
        slack('Copying replacement batches')
        subprocess.call(['rsync -rav --progress /opt/chronam/data/chronamftp/replacement_batches/* /opt/chronam/data/dlg_batches/drop/'])
        duration = time.time() - start_time
        slack('RSync of new and replacement batches completed in %s seconds' % duration)

        # LOAD NEW TITLES IF PRESENT
        if new_title_folders:
            slack('Also found `%s` title MARC files to process.' % len(new_title_folders))
            for nt in new_title_folders:
                for nt_f in os.listdir(os.path.join(new_batches_location, nt)):
                    if nt_f.endswith('.xml'):
                        marc_file = os.path.join(nonlccn_location, nt_f)
                        copyfile(
                            os.path.join(new_batches_location, nt, nt_f),
                            marc_file)
                        title_load_results = title_loader.load(marc_file)
                        if title_load_results[1]:
                            slack('New title created from `%s`.' % nt_f)
                        if title_load_results[2]:
                            slack('Title updated from `%s`.' % nt_f)
                        if title_load_results[3]:
                            slack('Error on title load from `%s`' % nt_f)
            index_titles(start)
            slack('Finished loading titles.')

        # PURGE REPLACEMENT BATCHES
        if replacement_batches:
            slack('Purging batches destined for replacement.')
            for r_b in replacement_batches:
                batch_to_purge = r_b.replace('ver02','ver01')\
                    .replace('ver03','ver02')\
                    .replace('ver04','ver03')\
                    .replace('ver05','ver04')\
                    .replace('ver06','ver05')\
                    .replace('ver07','ver06')\
                    .replace('ver08','ver07')
                slack('Purging `%s`.' % batch_to_purge)
                loader.purge_batch(batch_to_purge)
            start_time = time.time()
            solr = SolrConnection(settings.SOLR)
            solr.optimize()
            slack('Index optimize complete in `%s` seconds.' % time.time() - start_time)

        # LOAD ALL BATCHES
        # start with replacement batches
        final_loader = batch_loader.BatchLoader(process_ocr=True, process_coordinates=True)
        if replacement_batches:
            replace_start = time.time()
            for replacement in replacement_batches:
                final_loader.load_batch('drop/%s' % replacement, strict=False)
                slack('Loaded replacement batch `%s`.' % replacement)
            slack('All replacement batches loaded in `%s` seconds.' % time.time() - replace_start)
        # load new batches
        if new_batches:
            new_start = time.time()
            for new in new_batches:
                final_loader.load_batch('drop/%s' % new, strict=False)
                slack('Loaded new batch `%s`.' % new)
            slack('All new batches loaded in `%s` seconds.' % time.time() - new_start)

        slack('Batch loading job complete!')
