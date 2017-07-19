from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import urlresolvers
from django.db.models import Min, Max
from chronam.core.models import Region, Place, Title, NewspaperType, Issue

def region_page(request, region):

    region = get_object_or_404(Region, slug=region)

    page_title = region.name
    places = Place.objects.filter(state='Georgia', region=region)
    region_image = 'images/' + region.homepage_image
    region_text = region.homepage_copy

    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{
        'label': region.name,
        'href': urlresolvers.reverse('region_page', kwargs={'region': region.slug} )
    }])

    counties = []
    county_titles = []
    cities = []
    cities_with_titles = []
    all_titles = []

    for place in places:
        if not place.county in counties:
            if place.county:
                counties.append(place.county)
        if not place.city in cities:
            if place.city:
                cities.append(place.city)

    counties = sorted(counties)
    cities = sorted(cities)

    # available page range
    issue_dates = Issue.objects.filter(title__places__region=region).aggregate(min_date=Min('date_issued'), max_date=Max('date_issued'))
    if issue_dates['min_date'] and issue_dates['max_date']:
        start_year = issue_dates['min_date'].year
        end_year = issue_dates['max_date'].year
    else:
        start_year = None
        end_year = None

    for county in counties:
        if county:
            t = dict()
            t['county'] = county
            titles = Title.objects.filter(places__county__contains=county).order_by('+name').order_by('-start_year')
            t['titles'] = titles
            if t['titles']:
                county_titles.append(t)
                for title in titles:
                    all_titles.append(title)

    cities_with_titles_r = Place.objects.filter(titles__in=all_titles).values('city')

    cities_with_titles = []
    for city_with_title in cities_with_titles_r:
        if not city_with_title['city'] in cities_with_titles:
            cities_with_titles.append(city_with_title['city'])

    cities_with_titles = sorted(cities_with_titles)

    types = NewspaperType.objects.all

    return render_to_response('region.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))