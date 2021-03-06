from datetime import datetime

from django import forms
from django.forms import fields, ModelForm
from django.conf import settings
from django.core.cache import cache
from django.db.models import Min, Max

from chronam.core import models

MIN_YEAR = 1800
MAX_YEAR = 2500
DAY_CHOICES = [(i, i) for i in range(1,32)]
MONTH_CHOICES = ((1, u'Jan',), (2, u'Feb',), (3, u'Mar',),
                 (4, u'Apr',), (5, u'May',), (6, u'Jun',),
                 (7, u'Jul',), (8, u'Aug',), (9, u'Sep',),
                 (10, u'Oct',), (11, u'Nov',), (12, u'Dec',)) 

FREQUENCY_CHOICES = (
    ("", "Select"),
    ("Daily", "Daily"),
    ("Three times a week", "Three times a week"),
    ("Semiweekly", "Semiweekly"),
    ("Weekly", "Weekly"),
    ("Biweekly", "Biweekly"),
    ("Three times a month", "Three times a month"),
    ("Semimonthly", "Semimonthly"),
    ("Monthly", "Monthly"),
    ("Other", "Other"),
    ("Unknown", "Unknown"),
)

PROX_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("5", "5"),
    ("10", "10"),
    ("50", "50"),
    ("100", "100"),
)


def _regions_options():
    form_regions = cache.get("form_regions")
    if not form_regions:
        form_regions = [("", "All Regions")]
        for region in models.Region.objects.all():
            form_regions.append((region.slug, region.name))
        form_regions = sorted(form_regions)
        cache.set("form_regions", form_regions)
    return form_regions


def _types_options():
    form_types = cache.get("form_types")
    if not form_types:
        form_types = [("", "All Regions")]
        for type in models.NewspaperType.objects.all():
            form_types.append((type.slug, type.name))
        form_types = sorted(form_types)
        cache.set("form_types", form_types)
    return form_types


def _counties_options():
    # form_counties = cache.get("form_counties")
    # if not form_counties:
    form_counties = [("", "All Counties")]
    _counties = set()
    for title in models.Title.objects.filter(has_issues=True).select_related():
        for p in title.places.all():
            _counties.add(p.county)
    _counties = filter(lambda s: s is not None, _counties)
    for county in _counties:
        form_counties.append((county, county))
    form_counties = sorted(form_counties)
    cache.set("form_counties", form_counties)

    return form_counties


# return dict of id=>name for Cities in Places
def _cities_options():
    # form_cities = cache.get("form_cities")
    # if not form_cities:
    form_cities = [("", "All Cities")]
    _cities = set()
    for title in models.Title.objects.filter(has_issues=True).select_related():
        for p in title.places.all():
            _cities.add(p.city)
    _cities = filter(lambda s: s is not None, _cities)
    for city in _cities:
        form_cities.append((city, city))
    form_cities = sorted(form_cities)
    cache.set("form_cities", form_cities)

    return form_cities


def _titles_states():
    """
    returns a tuple of two elements (list of titles, list of states)

    example return value:
    ([('', 'All newspapers'), (u'sn83030214', u'New-York tribune. (New York [N.Y.])')], 
     [('', 'All states'), (u'New York', u'New York')])
    """
    titles_states = cache.get("titles_states")
    if not titles_states:
        titles = [("", "All newspapers"), ]
        states = [("", "All states")]
        # create a temp Set _states to hold states before compiling full list
        _states = set()
        for title in models.Title.objects.filter(has_issues=True).select_related():
            short_name = title.name.split(":")[0]  # remove subtitle
            title_name = "%s (%s)" % (short_name,
                                      title.place_of_publication)
            titles.append((title.lccn, title_name))
            for p in title.places.all():
                _states.add(p.state)
        _states = filter(lambda s: s is not None, _states)
        for state in _states:
            states.append((state, state))
        states = sorted(states)
        cache.set("titles_states", (titles, states))
    else:
        titles, states = titles_states
    return (titles, states)


def _titles_options():
    # titles = cache.get("titles")
    # if not titles:
    titles = [("", "All newspapers"), ]
    for title in models.Title.objects.filter(has_issues=True).order_by('name'):
        short_name = title.name.split(":")[0]  # remove subtitle
        title_name = "%s (%s)" % (short_name,
                                  title.place_of_publication)
        titles.append((title.lccn, title_name))
    cache.set("titles", titles)
    return titles


def _fulltext_range():
    # todo cached value was never changed...
    # fulltext_range = cache.get('fulltext_range')
    # if not fulltext_range:
    # get the maximum and minimum years that we have content for
    issue_dates = models.Issue.objects.all().aggregate(min_date=Min('date_issued'),
                                                       max_date=Max('date_issued'))

    # when there is no content these may not be set
    if issue_dates['min_date']:
        min_year = issue_dates['min_date'].year
    else:
        min_year = MIN_YEAR
    if issue_dates['max_date']:
        max_year = issue_dates['max_date'].year
    else:
        max_year = MAX_YEAR

    fulltext_range = (min_year, max_year)
    # cache.set('fulltext_range', fulltext_range)
    return fulltext_range


class SearchPagesForm(forms.Form):
    # state = fields.ChoiceField(choices=[])
    date1 = fields.ChoiceField(choices=[])
    date2 = fields.ChoiceField(choices=[])
    proxtext = fields.CharField()
    sequence = fields.BooleanField()
    issue_date = fields.BooleanField()

    def __init__(self, *args, **kwargs):
        super(SearchPagesForm, self).__init__(*args, **kwargs)

        # self.titles, self.states = _titles_states()

        # added by MK
        self.titles = _titles_options()
        self.cities = _cities_options()
        self.counties = _counties_options()
        self.types = _types_options()
        self.regions = _regions_options()

        fulltextStartYear, fulltextEndYear = _fulltext_range()

        self.years = [(year, year) for year in range(fulltextStartYear, fulltextEndYear + 1)]
        self.fulltextStartYear = fulltextStartYear
        self.fulltextEndYear = fulltextEndYear

        # self.fields["state"].choices = self.states
        self.fields["date1"].choices = self.years
        self.fields["date1"].initial = fulltextStartYear
        self.fields["date2"].choices = self.years
        self.fields["date2"].initial = fulltextEndYear
        self.fields["sequence"].widget.attrs['value'] = 1


class AdvSearchPagesForm(SearchPagesForm):
    date_month = fields.ChoiceField(choices=MONTH_CHOICES)
    date_day = fields.ChoiceField(choices=DAY_CHOICES)
    lccn = fields.MultipleChoiceField(choices=[])
    # state = fields.MultipleChoiceField(choices=[])
    city = fields.MultipleChoiceField(_cities_options())
    county = fields.MultipleChoiceField(_counties_options())
    newspaper_type = fields.MultipleChoiceField(_types_options())
    region = fields.MultipleChoiceField(_regions_options())

    date1 = fields.CharField()
    date2 = fields.CharField()
    sequence = fields.CharField()
    ortext = fields.CharField()
    andtext = fields.CharField()
    nottext = fields.CharField()
    proxtext = fields.CharField()
    proxdistance = fields.ChoiceField(choices=PROX_CHOICES)
    # language = fields.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(AdvSearchPagesForm, self).__init__(*args, **kwargs)

        self.date = self.data.get('date1', '')

        self.fields["city"].choices = self.cities
        self.fields["county"].choices = self.counties
        self.fields["newspaper_type"].choices = self.types
        self.fields["region"].choices = self.regions
        self.fields["lccn"].choices = self.titles
        # self.fields["state"].widget.attrs = {'id': 'id_states'}
        self.fields["date1"].widget.attrs = {"id": "id_date_from", "max_length": 10}
        self.fields["date1"].initial = ""
        self.fields["date2"].widget.attrs = {"id": "id_date_to", "max_length": 10}
        self.fields["date2"].initial = ""
        self.fields["proxdistance"].initial = "5"
        # self.fields["city"].widget.attrs = {"data-placeholder": "Click here to choose some Cities"}
        # self.fields["county"].widget.attrs = {"data-placeholder": "Click here to choose some Counties"}
        # self.fields["newspaper_type"].widget.attrs = {"data-placeholder": "Click here to choose some Types"}
        # self.fields["region"].widget.attrs = {"data-placeholder": "Click here to choose some Regions"}
        self.fields["lccn"].widget.attrs = {'id': 'id_lccns'}
        self.fields["sequence"].widget.attrs = {"id": "id_char_sequence", "size": "3"}
        self.fields["proxtext"].widget.attrs = {"id": "id_proxtext_adv", "class": "form-control"}
        self.fields["ortext"].widget.attrs = {"class": "form-control"}
        self.fields["andtext"].widget.attrs = {"class": "form-control"}
        self.fields["nottext"].widget.attrs = {"class": "form-control"}
        # lang_choices = [("", "All"), ]
        # lang_choices.extend((l, models.Language.objects.get(code=l).name) for l in settings.SOLR_LANGUAGES)
        # self.fields["language"].choices = lang_choices


class SearchTitlesForm(forms.Form):
    # state = fields.ChoiceField(choices=[], initial="")
    county = fields.ChoiceField(choices=[], initial="")
    city = fields.ChoiceField(choices=[], initial="")
    year1 = fields.ChoiceField(choices=[], label="from")
    year2 = fields.ChoiceField(choices=[], label="to")
    terms = fields.CharField(max_length=255)
    frequency = fields.ChoiceField(choices=FREQUENCY_CHOICES, initial="", label="Frequency:")
    language = fields.ChoiceField(choices=[], initial="", label="Language:")
    ethnicity = fields.ChoiceField(choices=[], initial="", label="Ethnicity Press:")
    labor = fields.ChoiceField(choices=[], initial="", label="Labor Press:")
    material_type = fields.ChoiceField(choices=[], initial="", label="Material Type:")
    lccn = fields.CharField(max_length=255, label="LCCN:")

    def __init__(self, *args, **kwargs):
        super(SearchTitlesForm, self).__init__(*args, **kwargs)
        current_year = datetime.date.today().year
        years = range(1690, current_year + 1, 10)
        if years[-1] != current_year:
            years.append(current_year)
        choices = [(year, year) for year in years]
        self.fields["year1"].choices = choices
        self.fields["year1"].widget.attrs["class"] = "norm"
        self.fields["year1"].initial = choices[0][0]
        self.fields["year2"].choices = choices
        self.fields["year2"].initial = choices[-1][0]
        self.fields["year2"].widget.attrs["class"] = "norm"

        language = [("", "Select"), ]
        language.extend((l.name, l.name) for l in models.Language.objects.all())
        self.fields["language"].choices = language

        ethnicity = [("", "Select"), ]
        ethnicity.extend((e.name, e.name) for e in models.Ethnicity.objects.all())
        self.fields["ethnicity"].choices = ethnicity

        labor = [("", "Select"), ]
        labor.extend((l.name, l.name) for l in models.LaborPress.objects.all())
        self.fields["labor"].choices = labor

        material = [("", "Select")]
        material.extend((m.name, m.name) for m in models.MaterialType.objects.all())
        self.fields["material_type"].choices = material
