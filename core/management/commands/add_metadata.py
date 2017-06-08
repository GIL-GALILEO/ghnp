import sys
import simplejson as json

from django.core.management.base import BaseCommand, CommandError
from chronam.core.models import Title, Region, FundingSource, NewspaperType

class Command(BaseCommand):
    help = 'Adds custom GHNP metadata to title records by LCCN'

    def add_arguments(self, parser):
        parser.add_argument(
            '--lccns',
            dest='lccns',
            default='',
            help='Provide Title llcns to receive additional metadata'
        )
        parser.add_argument(
            '--json',
            dest='json_path',
            default='',
            help='Provide path to JSON file containing additional metadata'
        )

    def handle(self, *args, **options):

        # get Titles
        lccns = options['lccns'].split(',')
        try:
            titles = [Title.objects.get(lccn=lccn) for lccn in lccns]
        except:
            raise CommandError('At least one of your LCCNs could not be found')

        # get data from JSON file
        try:
            with open(options['json_path'], 'rb') as f:
                data = json.load(f)
            funding_source_code = data.get('funding_source').strip()
            newspaper_type_codes = data.get('newspaper_types')
            essay_text = data.get('essay').strip()
        except IOError, _:
            raise CommandError('Problem reading JSON file at %s' % options['json_path'])
        except json.JSONDecodeError, e:
            raise CommandError('JSON parsing error: %s' % e)

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
            except:
                e = sys.exc_info()[0]
                raise CommandError('Problem saving title with lccn %s: %s' % (title.lccn, e))

        self.stdout.write('Task complete. %s titles updated.' % len(titles))



