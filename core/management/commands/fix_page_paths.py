import os
import logging

from optparse import make_option
from django.core.management.base import BaseCommand
from chronam.core.management.commands import configure_logging
from chronam.core.models import Page
from django.conf import settings

configure_logging('fix_pages.config',
                  'fix_pages_%s.log' % os.getpid())

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--save',
                    action='store_true',
                    dest='save', default=False,
                    help='Save Pages after updating'),
    )
    help = "Fix full paths on some Page records."

    def handle(self, *args, **options):

        pages = Page.objects.all()
        bsp = settings.BATCH_STORAGE
        paths_fixed = 0

        for page in pages:
            if bsp in page.jp2_filename:
                page.jp2_filename = page.jp2_filename[page.jp2_filename.rfind('data/') + 5:]
                paths_fixed += 1
            if bsp in page.tiff_filename:
                page.tiff_filename = page.tiff_filename[page.tiff_filename.rfind('data/') + 5:]
                paths_fixed += 1
            if bsp in page.pdf_filename:
                page.pdf_filename = page.pdf_filename[page.pdf_filename.rfind('data/') + 5:]
                paths_fixed += 1
            if bsp in page.ocr_filename:
                page.ocr_filename = page.ocr_filename[page.ocr_filename.rfind('data/') + 5:]
                paths_fixed += 1
            if options['save']:
                page.save()

        _logger.info("Paths fixed: %s", paths_fixed)





