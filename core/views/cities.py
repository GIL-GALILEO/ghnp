from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import urlresolvers
from chronam.core.models import Region, Place, Title, NewspaperType

def cities_page(request):

    page_title = 'Browse by City'
    places = Place.objects.filter(state='Georgia')

    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{
        'label': page_title,
    }])

    counties = []
    county_titles = []
    cities = []
    cities_with_titles = []
    all_titles = []

    for place in places:
        if not place.county in counties:
            counties.append(place.county)
        if not place.city in cities:
            cities.append(place.city)

    for county in counties:
        if county:
            t = dict()
            t['county'] = county
            titles = Title.objects.filter(places__county__contains=county)
            t['titles'] = titles
            if t['titles']:
                county_titles.append(t)
                for title in titles:
                    all_titles.append(title)

    cities_with_titles = Place.objects.filter(titles__in=all_titles).values('city')

    types = NewspaperType.objects.all

    return render_to_response('cities.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))

def city_page(request):

    return