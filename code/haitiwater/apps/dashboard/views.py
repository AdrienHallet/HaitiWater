from django.http import HttpResponse
from django.template import loader

from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME
from ..utils.get_data import *


def index(request):
    template = loader.get_template('dashboard.html')
    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
    }
    if request.user.is_authenticated:
        context['water_outlets_report'] = get_outlets_report(request)
        if request.user.profile.zone:  # Gestionnaire de zone
            context['zone_name'] = request.user.profile.zone.name
            context['amount_fountain'] = get_amount_fountain(request.user.profile.zone)
            context['amount_kiosk'] = get_amount_kiosk(request.user.profile.zone)
            context['amount_individual'] = get_amount_individual(request.user.profile.zone)
            context['amount_pipe'] = get_amount_pipe(request.user.profile.zone)
            context['amount_registered_consumers'] = get_amount_household(request)
            context['amount_individual_consumers'] = get_total_consumers(request)

    return HttpResponse(template.render(context, request))
