from django.http import HttpResponse
from django.template import loader
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME
from ..utils.get_data import get_zone


def index(request):
    template = loader.get_template('zone_management.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': get_zone(request)
    }
    return HttpResponse(template.render(context, request))

def logs(request):
    template = loader.get_template('logs.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    return HttpResponse(template.render(context, request))
