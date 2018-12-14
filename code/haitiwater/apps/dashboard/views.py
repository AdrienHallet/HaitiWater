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
    }
    if request.user.is_authenticated:
        context['zone_name'] = request.user.profile.zone.name
        context['amount_fountain'] = get_amount_fountain(request.user.profile.zone)
        context['amount_kiosk'] = get_amount_kiosk(request.user.profile.zone)
        context['amount_individual'] = get_amount_individual(request.user.profile.zone)
        context['amount_pipe'] = get_amount_pipe(request.user.profile.zone)
        context['amount_registered_consumers'] = get_amount_consumer(request.user.profile.zone)
        context['amount_individual_consumers'] = get_amount_indiv_consummer(request.user.profile.zone)
    return HttpResponse(template.render(context, request))

#TODO zone
def get_amount_fountain(zone):
    return len(Element.objects.filter(type="FOUNTAIN"))

def get_amount_kiosk(zone):
    return len(Element.objects.filter(type="KIOSK"))

def get_amount_individual(zone):
    return len(Element.objects.filter(type="INDIVIDUAL"))

def get_amount_pipe(zone):
    return len(Element.objects.filter(type="PIPE"))

def get_amount_consumer(zone):
    return len(Consumer.objects.all())

def get_amount_indiv_consummer(zone):
    result = 0
    for consumer in Consumer.objects.all():
        result += consumer.household_size
    return result
