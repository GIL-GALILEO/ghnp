from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from chronam.core.models import Region, Place, Title

def regions(request, region=None):

    if region:
        region = get_object_or_404(Region, slug=region)
        page_title = '%s Newspapers' % region.name
        places = Place.objects.filter(state='Georgia', region=region)
    else:
        page_title = 'Browse Newspapers by Region'
        places = Place.objects.filter(state='Georgia')

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

    return render_to_response('regions.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))