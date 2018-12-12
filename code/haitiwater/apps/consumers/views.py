from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('consumers.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': 'Nom de la zone',  # Todo Backend
        'current_period': 'Septembre',  # Todo Backend (month of current computed paid info)
        'water_outlets': get_outlets()
    }
    return HttpResponse(template.render(context, request))

def get_outlets():
    all_outlets = Element.objects.all()
    result = []
    for elem in all_outlets:
        if elem.type in ["KIOSK", "FOUNTAIN", "INDIVIDUAL"]:
            result.append((elem.id, elem.name))
    return result