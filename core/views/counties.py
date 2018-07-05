from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from chronam.core.models import Place, Title, Issue, NewspaperType
from django.db.models import Min, Max

from django.core import urlresolvers

import collections


def counties_page(request):
    page_title = 'Browse by County'
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{
        'label': page_title,
    }])
    counties_with_titles = Place.objects.filter(titles__in=Title.objects.all).filter(city__isnull=False).distinct().order_by('county').values_list('county', flat=True)
    counties_with_titles_by_letter = collections.OrderedDict()
    for c in counties_with_titles:
        county_titles = {
            'county': c,
            'titles': Title.objects.filter(places__county=c)
        }
        first_letter = c[:1]
        if first_letter in counties_with_titles_by_letter:
            counties_with_titles_by_letter[first_letter].append(county_titles)
        else:
            counties_with_titles_by_letter[first_letter] = [county_titles]

    return render_to_response('counties.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))


def county_page(request, county):

    # validate county
    place = get_object_or_404(Place.objects.filter(county=county.title(), titles__has_issues='true').first())

    county = place.county

    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{
        'label': 'Browse by County',
        'href': urlresolvers.reverse('browse_by_county', kwargs={} )
    },{
        'label': county,
        'href': urlresolvers.reverse('county_page', kwargs={'county': county} )
    }])

    cities = Place.objects.filter(county=county).distinct('city').order_by('city')
    all_titles = []

    # available page range
    issue_dates = Issue.objects.filter(title__places__county=county).aggregate(min_date=Min('date_issued'), max_date=Max('date_issued'))
    if issue_dates['min_date'] and issue_dates['max_date']:
        start_year = issue_dates['min_date'].year
        end_year = issue_dates['max_date'].year
    else:
        start_year = None
        end_year = None

    titles_in_county = Title.objects.filter(places__county=county).order_by('+name').order_by('-start_year')

    return render_to_response('county.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))
