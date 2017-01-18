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
        places = Place.objects.all(state='Georgia')


    counties = []
    for place in places.values('county'):
        if not place['county'] in counties:
            counties.append(place['county'])


    county_titles = []
    for c in counties:
        titles = dict()
        titles['county'] = c
        titles['titles'] = Title.objects.filter(places__county__contains=c)
        county_titles.append(titles)

    return render_to_response('regions.html', dictionary=locals(),
                              context_instance=RequestContext(request))