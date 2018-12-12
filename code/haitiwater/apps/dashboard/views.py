from django.http import HttpResponse
from django.template import loader
from ..water_network.models import Element
from ..consumers.models import Consumer
from django.template.loader import render_to_string
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('dashboard.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'zone_name': 'Nom de la zone',  # Todo backdend
        'amount_fountain': get_amount_fountain(),
        'amount_kiosk': get_amount_kiosk(),
        'amount_individual': get_amount_individual(),
        'amount_pipe': get_amount_pipe(),
        'amount_registered_consumers': get_amount_consumer(),
        'amount_individual_consumers': get_amount_indiv_consummer()
    }
    return HttpResponse(template.render(context, request))
#TODO zone
def get_amount_fountain():
    return len(Element.objects.filter(type="FOUNTAIN"))

def get_amount_kiosk():
    return len(Element.objects.filter(type="KIOSK"))

def get_amount_individual():
    return len(Element.objects.filter(type="INDIVIDUAL"))

def get_amount_pipe():
    return len(Element.objects.filter(type="PIPE"))

def get_amount_consumer():
    return len(Consumer.objects.all())

def get_amount_indiv_consummer():
    result = 0
    for consumer in Consumer.objects.all():
        result += consumer.household_size
    return result
