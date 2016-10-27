import os
import logging

from django.core.management.base import BaseCommand

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

        metro_atlanta_counties = ['Clayton', 'Cobb', 'DeKalb', 'Fulton', 'Gwinnett', 'Henry', 'Rockdale']
        north_georgia_counties = ['Banks', 'Barrow', 'Bartow', 'Catoosa', 'Chattooga', 'Cherokee', 'Clarke', 'Dade', 'Dawson', 'Elbert', 'Fannin', 'Floyd', 'Forsyth', 'Franklin', 'Gilmer', 'Gordon', 'Habersham', 'Hall', 'Hart', 'Jackson', 'Lumpkin', 'Madison', 'Morgan', 'Murray', 'Newton', 'Oconee', 'Oglethorpe', 'Pickens', 'Polk', 'Rabun', 'Stephens', 'Towns', 'Union', 'Walker', 'Walton', 'White', 'Whitfield']
        west_georgia_counties = ['Carroll', 'Chattahoochee', 'Coweta', 'Douglas', 'Fayette', 'Haralson', 'Harris', 'Heard', 'Macon', 'Marion', 'Meriwether', 'Muscogee', 'Paulding', 'Pike', 'Schley', 'Spalding', 'Stewart', 'Sumter', 'Talbot', 'Taylor', 'Troup', 'Upson', 'Webster']
        middle_georgia_counties = ['Baldwin', 'Bibb', 'Bleckley', 'Butts', 'Crawford', 'Dodge', 'Dooly', 'Houston', 'Jasper', 'Jones', 'Lamar', 'Laurens', 'Monroe', 'Peach', 'Pulaski', 'Putnam', 'Twiggs', 'Wilkinson']
        east_georgia_counties = ['Burke', 'Columbia', 'Emanuel', 'Glascock', 'Greene', 'Hancock', 'Jefferson', 'Jenkins', 'Johnson', 'Lincoln', 'McDuffie', 'Richmond', 'Taliaferro', 'Warren', 'Washington', 'Wilkes']
        south_georgia_counties = ['Appling', 'Atkinson', 'Bacon', 'Baker', 'Ben Hill', 'Berrien', 'Brantley', 'Brooks', 'Bryan', 'Bulloch', 'Calhoun', 'Camden', 'Candler', 'Charlton', 'Chatham', 'Clay', 'Clinch', 'Coffee', 'Colquitt', 'Cook', 'Crisp', 'Decatur', 'Dougherty', 'Early', 'Echols', 'Effingham', 'Evans', 'Glynn', 'Grady', 'Irwin', 'Jeff Davis', 'Lanier', 'Lee', 'Liberty', 'Long', 'Lowndes', 'McIntosh', 'Miller', 'Mitchell', 'Montgomery', 'Pierce', 'Quitman', 'Randolph', 'Screven', 'Seminole', 'Tattnall', 'Telfair', 'Terrell', 'Thomas', 'Tift', 'Toombs', 'Treutlen', 'Turner', 'Ware', 'Wayne', 'Wheeler', 'Wilcox', 'Worth']

        places = Place.objects.all().filter(
            name__startswith='Georgia'
        )

        metro_atlanta = Region.objects.get(name='Metro Atlanta')
        north_georgia = Region.objects.get(name='North Georgia')
        west_georgia = Region.objects.get(name='West Georgia')
        middle_georgia = Region.objects.get(name='Middle Georgia')
        east_georgia = Region.objects.get(name='East Georgia')
        south_georgia = Region.objects.get(name='South Georgia')

        for place in places:
            _logger.info("Place: %s" % place.name)
            name_parts = place.name.split('--')
            if len(name_parts) == 3:
                place.state = name_parts[0]
                place.county = name_parts[1]
                place.city = name_parts[2]

                if place.county in metro_atlanta_counties:
                    place.region = metro_atlanta
                elif place.county in north_georgia_counties:
                    place.region = north_georgia
                elif place.county in west_georgia_counties:
                    place.region = west_georgia
                elif place.county in middle_georgia_counties:
                    place.region = middle_georgia
                elif place.county in east_georgia_counties:
                    place.region = east_georgia
                elif place.county in south_georgia_counties:
                    place.region = south_georgia
                else:
                    _logger.warn("County could not be mapped to a region: %s" % place.county)

                place.save()

            elif len(name_parts) == 2:

                place.state = name_parts[0]
                place.city = name_parts[1]
            else:
                _logger.warn("Name could not be parsed as expected: %s" % place.name)

            place.country = 'United States of America'
            place.save()

        _logger.info("Georgia places found: %s" % places.count())




