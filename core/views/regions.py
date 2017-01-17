from django.shortcuts import render_to_response
from django.template import RequestContext

def regions(request, region=None):
    if region:
        region = region
    else:
        region = 'All'
    return render_to_response('regions.html', dictionary=locals(),
                              context_instance=RequestContext(request))