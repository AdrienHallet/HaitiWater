from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..report.models import Report
from ..utils.get_data import *
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('report.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'current_period': 'Septembre',  # Todo Backend
        'water_outlets': get_outlets(request)
    }
    return HttpResponse(template.render(context, request))
