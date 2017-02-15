from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import urlresolvers
from chronam.core.models import Region, Place, Title

def regions(request, region=None):

    page_title = 'Browse by Region'
    places = Place.objects.filter(state='Georgia')

    region_image = 'images/state_counties.png'

    crumbs = list(settings.BASE_CRUMBS)
    crumbs.append({
        'label': 'Browse by Location',
        'href': urlresolvers.reverse('regions')
    })

    return render_to_response('regions.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))


def region_page(request, region):

    region = get_object_or_404(Region, slug=region)

    page_title = region.name
    places = Place.objects.filter(state='Georgia', region=region)
    region_image = 'images/' + region.homepage_image
    region_text = region.homepage_copy

    crumbs = list(settings.BASE_CRUMBS)
    crumbs.append({
        'label': 'Browse by Location',
        'href': urlresolvers.reverse('regions')
    })
    crumbs.append({
        'label': region.name,
        'href': urlresolvers.reverse('region_page', kwargs={'region': region.slug} )
    })

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

    return render_to_response('region.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))