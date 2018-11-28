from django.http import HttpResponse
from django.template import loader
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('consumers.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': 'Nom de la zone',  # Todo Backend
        'current_period': 'Septembre',  # Todo Backend (month of current computed paid info)
        'water_outlets': [(1, 'Fontaine Bidule'), (2, 'Kiosque Machin'), (3, 'Prise Truc')] # Todo Backend (see report/views.py, it is the same)
    }
    return HttpResponse(template.render(context, request))
