from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..report.models import Report
from ..utils.get_data import *
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def index(request):
    template = loader.get_template('report.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'current_period': get_current_month_fr(),
        'water_outlets_ticket': get_outlets(request),
        'water_outlets_report': get_outlets_report(request)
    }
    return HttpResponse(template.render(context, request))
