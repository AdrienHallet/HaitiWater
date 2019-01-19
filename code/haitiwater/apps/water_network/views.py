from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..consumers.models import Consumer
from ..report.models import Report
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME
from ..utils.get_data import *


def index(request):
    template = loader.get_template('water_network.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': get_zone(request),
        'consumers': get_total_consumers(request),
        'water_outlets': len(get_outlets(request)),
        'current_period': get_current_month_fr(),
        'distributed': get_quantity_distributed(request)
    }
    return HttpResponse(template.render(context, request))
