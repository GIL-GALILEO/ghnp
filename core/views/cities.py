from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from chronam.core.models import Place, Title

def cities_page(request):

    page_title = 'Browse by City'
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{
        'label': page_title,
    }])

    cities_with_titles = Place.objects.filter(titles__in=Title.objects.all).values('city')
    cities_with_titles_by_letter = {}

    for c in cities_with_titles:

        city_name = c['city']

        city_titles = {
            'city': city_name,
            'titles': Title.objects.filter(places__city=city_name)
        }

        first_letter = city_name[:1]

        if first_letter in cities_with_titles_by_letter:
            cities_with_titles_by_letter[first_letter].append(city_titles)
        else:
            cities_with_titles_by_letter[first_letter] = [city_titles]

    return render_to_response('cities.html',
                              dictionary=locals(),
                              context_instance=RequestContext(request))

def city_page(request):

    return