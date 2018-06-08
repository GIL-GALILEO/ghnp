import sys
import simplejson as json
import os
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from chronam.core.models import Title, FundingSource, NewspaperType
from django.db.utils import IntegrityError
from chronam.core.management.commands import configure_logging

configure_logging('sync_extra_metadata.config',
                  'sync_extra_metadata_%s.log' % os.getpid())

LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Adds custom GHNP metadata to title records by LCCN'

    def handle(self, *args, **options):

        files_processed = 0
        json_path = settings.EXTRA_METADATA

        # iterate through each file
        if not os.path.isdir(json_path):
            raise CommandError('EXTRA_METADATA path in settings.py is not a directory!')

        json_dir = os.listdir(json_path)

        for json_file in json_dir:
            if os.path.isdir(json_file):
                continue
            # get data from JSON file
            try:
                with open(os.path.join(json_path, json_file), 'rb') as f:
                    data = json.load(f)
                lccns = data.get('lccn')
                funding_source_code = data.get('funding_source').strip()
                newspaper_type_codes = data.get('newspaper_types')
                essay_text = data.get('essay').strip()
            except IOError, _:
                LOGGER.error('Problem reading JSON file at %s' % options['json_path'])
                continue
            except json.JSONDecodeError, e:
                LOGGER.error('JSON parsing error at %s: %s' % (options['json_path'] % e))
                continue

            # get titles from lccns
            titles = []
            for lccn in lccns:
                try:
                    titles.append(Title.objects.get(lccn=lccn))
                except Title.DoesNotExist:
                    LOGGER.error('No existing title found for %s in %s' % (lccn, json_file))
                    continue

            # get NewspaperType objects
            try:
                newspaper_types = [NewspaperType.objects.get(slug=code) for code in newspaper_type_codes]
            except:
                raise CommandError('Newspaper Type "%s" could not be found' % code)

            # get FundingSource object
            if funding_source_code:
                try:
                    funding_source = FundingSource.objects.get(slug=funding_source_code)
                except:
                    raise CommandError('Funding Source "%s" could not be found' % funding_source_code)

            # apply to titles
            for title in titles:
                try:
                    if newspaper_types: title.newspaper_types = newspaper_types
                    if funding_source_code: title.funding_source = funding_source
                    if essay_text: title.essay_text = essay_text
                    title.save()
                except IntegrityError as e:
                    raise CommandError('Problem saving title with lccn %s: %s' % (title.lccn, format(e.errno, e.strerror)))
                except:
                    e = sys.exc_info()[0]
                    raise CommandError('Problem saving title with lccn %s: %s' % (title.lccn, e))

            LOGGER.info('Sync complete for file %s. %i titles updated.' % (json_file, len(titles)))

            files_processed += 1

        self.stdout.write('JSON files synced: %i' % files_processed)