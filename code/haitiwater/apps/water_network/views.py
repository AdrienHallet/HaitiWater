from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..consumers.models import Consumer
from ..report.models import Report
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('water_network.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': "Nom de la zone",  # Todo Backend
        'consumers': get_consumers(),
        'water_outlets' : get_outlets(),
        'distributed' : get_quantity()
    }
    return HttpResponse(template.render(context, request))

#TODO zone
def get_consumers():
    all_consumer = Consumer.objects.all()
    result = 0
    for elem in all_consumer:
        result += elem.household_size
    return result

def get_outlets():
    all_outlets = Element.objects.filter(type__in=["KIOSK", "FOUNTAIN", "INDIVIDUAL"])
    result = []
    for elem in all_outlets:
        result.append((elem.id, elem.name))
    return result

def get_quantity():
    all_outlets = Element.objects.filter(type__in=["KIOSK", "FOUNTAIN", "INDIVIDUAL"])
    result = 0
    for elem in all_outlets:
        reports = Report.objects.filter(water_outlet=elem.id)
        for report in reports:
            result += report.quantity_distributed
    return result