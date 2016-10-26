import os
import logging

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from chronam.core import batch_loader
from chronam.core.management.commands import configure_logging
from chronam.core.models import Place, Region

configure_logging('refine_places_logging.config',
                  'refine_places_%s.log' % os.getpid())

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    )
    help = "Parse place names and update city, county and state values. Also add region if possible."

    def handle(self, *args, **options):

        places = Place.objects.all().filter(
            name__startswith='Georgia'
        )

        for place in places:
            _logger.info("Place: %s" % place.name)
            name_parts = place.name.split('--')
            if name_parts.count() == 3:
                place.state = name_parts[0]
                place.county = name_parts[1]
                place.city = name_parts[2]
                place.save()
            else:
                _logger.warn("Name could not be parsed as expected: %s" % place.name)


        _logger.info("Georgia places found: %s" % places.count())




