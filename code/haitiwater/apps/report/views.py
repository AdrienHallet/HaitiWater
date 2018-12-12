from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..report.models import Report
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('report.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'current_period': 'Septembre',  # Todo Backend
        'water_outlets': get_outlets()
    }
    return HttpResponse(template.render(context, request))

def get_outlets():
    all_outlets = Element.objects.all()
    result = []
    for elem in all_outlets:
        if elem.type in ["KIOSK", "FOUNTAIN", "INDIVIDUAL"]:
            reports = Report.objects.filter(water_outlet=elem.id) #TODO add filter by month
            if len(reports) == 0:
                result.append((elem.id, elem.name))
    return result
