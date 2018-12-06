from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('dashboard.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': 'Nom de la zone',  # Todo backdend
        'amount_fountain': 42,  # Todo backend
        'amount_kiosk': 42,  # Todo backend
        'amount_individual': 42,  # Todo backend
        'amount_pipe': 42,  # Todo backend
        'amount_registered_consumers': 20,  # Todo backend
        'amount_individual_consumers': 40,  # Todo backend
    }
    return HttpResponse(template.render(context, request))
