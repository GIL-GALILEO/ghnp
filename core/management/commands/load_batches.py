import os
import logging
from datetime import datetime
from optparse import make_option

from django.conf import settings
from chronam.core.models import Batch
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from chronam.core import batch_loader
from chronam.core.management.commands import configure_logging

from slackclient import SlackClient

configure_logging('load_batches_logging.config', 
                  'load_batches_%s.log' % os.getpid())

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

    def handle(self, batch_list_filename, *args, **options):
        def slack(message):
            sc.api_call("chat.postMessage", channel="#ghnp", text=message)

        def log(message):
            _logger.info(message.replace('`', ''))

        def update(message):
            slack(message)
            log(message)

        if len(args) != 0:
            raise CommandError('Usage is load_batch %s' % self.args)

        added_batches = []
        failed_batches = []
        skipped_batches = []
        processed = 0
        start = datetime.now()

        sc = SlackClient(settings.SLACK_KEY)

        loader = batch_loader.BatchLoader(process_ocr=options['process_ocr'],
                                          process_coordinates=options['process_coordinates'])

        # get legit batch names
        with open(batch_list_filename) as f:
            batch_names_from_file = f.readlines()
            batch_names_from_file[:] = [batch_name for batch_name in batch_names_from_file if batch_name.strip()]
            count = len(batch_names_from_file)

        update('Loading `%s` Batches from file: `%s`' % (count, batch_list_filename))
        for line in batch_names_from_file:
            batch_start = datetime.now()
            processed += 1
            batch_name = line.strip()
            update('Loading batch `%s` of `%s`: `%s`' % (processed, count, batch_name))
            try:
                if Batch.objects.filter(name=batch_name).count() != 0:
                    skipped_batches.append(batch_name)
                    continue
                batch = loader.load_batch(batch_name, strict=False)
                added_batches.append(batch_name)
                update('`%s` loaded in `%s`.' % (batch_name, datetime.now() - batch_start))
            except Exception, e:
                update('`%s` failed to load. Error: `%s`.' % (batch_name, str(e)))
                failed_batches.append(batch_name)
                continue

        # create and write list of failed batches
        # TODO: not working IOError: [Errno 13] Permission denied: '/FAILED_all_batches_load.txt'
        # if len(failed_batches) > 0:
        #     failed_file_name = os.path.dirname(batch_list_filename) + '/FAILED_' + os.path.basename(batch_list_filename)
        #     with open(failed_file_name, 'w') as ff:
        #         for failed_batch in failed_batches:
        #             ff.write(failed_batch + "\n")
        #
        #     update('List of failed batches @ `%s`' % failed_file_name)

        # all done
        update('Run complete in `%s`. `%s` batches added, `%s` failed and `%s` skipped.' % (datetime.now() - start, len(added_batches), len(failed_batches), len(skipped_batches)))