from django.http import HttpResponse
from django.template import loader
from ..utils.get_data import get_zone, get_outlets, get_current_month
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('consumers.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': get_zone(request),
        'current_period': get_current_month(),
        'consumer_groups': 42,  # Todo Backend, only registered consumers
        'consumer_individuals': 42,  # Todo backend, total of registered consumers and their dependant persons
        'unpaid_bills': 42,  # Todo, but for later as we can't mark a payment yet
    }
    return HttpResponse(template.render(context, request))