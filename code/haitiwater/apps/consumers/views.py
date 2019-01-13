from django.http import HttpResponse
from django.template import loader
from ..utils.get_data import *
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('consumers.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': get_zone(request),
        'current_period': get_current_month_fr(),
        'water_outlets': get_outlets(request),
        'consumer_groups': get_registered_consumers(request),
        'consumer_individuals': get_total_consumers(request),
        'unpaid_bills': 42,  # Todo, but for later as we can't mark a payment yet
    }
    return HttpResponse(template.render(context, request))