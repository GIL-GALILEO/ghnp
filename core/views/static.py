from django.conf import settings
from django.core import urlresolvers
from chronam.core.decorator import cache_page
from django.shortcuts import render_to_response
from django.template import RequestContext

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about(request):
    page_title = "About Georgia Historic Newspapers"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'active': True},
    ])
    return render_to_response('about.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about_contactus(request):
    page_title = "Contact Us"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'href': urlresolvers.reverse('about')},
        {'label':'Contact Us',
         'active': True},
    ])
    return render_to_response('contact_us.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about_partners(request):
    page_title = "Partners"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'href': urlresolvers.reverse('about')},
        {'label':'Partners',
         'active': True},
    ])
    return render_to_response('partners.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about_resources(request):
    page_title = "Additional Resources"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'href': urlresolvers.reverse('about')},
        {'label':'Additional Resources',
         'active': True},
    ])
    return render_to_response('resources.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def about_copyright(request):
    page_title = "Copyright and Reuse"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'About',
         'href': urlresolvers.reverse('about')},
        {'label':'Copyright and Reuse',
         'active': True},
    ])
    return render_to_response('copyright.html', dictionary=locals(),
                              context_instance=RequestContext(request))


@cache_page(settings.DEFAULT_TTL_SECONDS)
def help_faq(request):
    page_title = "Frequently Asked Questions"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'Help',
         'active': True},
    ])
    return render_to_response('faq.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def help_browsing(request):
    page_title = "Help with Browsing"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'Help',
         'active': True},
    ])
    return render_to_response('browsing.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def help_searching(request):
    page_title = "Help with Searching"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'Help',
         'active': True},
    ])
    return render_to_response('searching.html', dictionary=locals(),
                              context_instance=RequestContext(request))

@cache_page(settings.DEFAULT_TTL_SECONDS)
def participate(request):
    page_title = "Participate"
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label':'Participate',
         'active': True},
    ])
    return render_to_response('participate.html', dictionary=locals(),
                              context_instance=RequestContext(request))


# @cache_page(settings.DEFAULT_TTL_SECONDS)
# def about_api(request):
#     page_title = "About the Site and API"
#     crumbs = list(settings.BASE_CRUMBS)
#     crumbs.extend([
#         {'label':'About API',
#          'href': urlresolvers.reverse('chronam_about_api'),
#          'active': True},
#     ])
#     return render_to_response('about_api.html', dictionary=locals(),
#                               context_instance=RequestContext(request))