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
    cities = []
    for place in places.values('county','city'):
        if not place['county'] in counties:
            counties.append(place['county'])
        if not place['city'] in cities:
            cities.append(place['city'])

    county_titles = []
    for county in counties:
        if county:
            titles = dict()
            titles['county'] = county
            titles['titles'] = Title.objects.filter(places__county__contains=county)
            county_titles.append(titles)

    return render_to_response('regions.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))