import os
import logging

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from chronam.core.batch_loader import BatchLoader, BatchLoaderException
from chronam.core.management.commands import configure_logging
    
configure_logging('load_batch_logging.config', 
                  'load_batch_%s.log' % os.getpid())

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--skip-process-ocr', 
                    action='store_false', 
                    dest='process_ocr', default=True,
                    help='Do not generate ocr, and index'),
        make_option('--skip-coordinates', 
                    action='store_false', 
                    dest='process_coordinates', default=True,
                    help='Do not out word coordinates'),
        make_option('--in-copyright',
                    dest='in_copyright', default=False,
                    help='Do not make available via API'),
    )

    help = "Load a batch"
    args = '<batch name>'

    def handle(self, batch_name, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is load_batch %s' % self.args)

        loader = BatchLoader(process_ocr=options['process_ocr'],
                             process_coordinates=options['process_coordinates'],
                             in_copyright=options['in_copyright'])
        try:
            batch = loader.load_batch(batch_name)
        except BatchLoaderException, e:
            LOGGER.exception(e)
            raise CommandError("unable to load batch. check the load_batch log for clues")
