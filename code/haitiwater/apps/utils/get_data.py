import datetime

from ..consumers.models import Consumer
from ..report.models import Report
from ..water_network.models import Element, VirtualElementTotal, VirtualZoneTotal


def is_int(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


def is_float(i):
    try:
        float(i)
        return True
    except ValueError:
        return False


def is_user_fountain(request):
    groups = request.user.groups.values_list('name', flat=True)
    return "Gestionnaire de fontaine" in groups


def is_user_zone(request):
    groups = request.user.groups.values_list('name', flat=True)
    return "Gestionnaire de zone" in groups


def get_current_month():
    today = datetime.date.today()
    months = ['zero', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    return months[today.month].upper()


def get_current_month_fr():
    today = datetime.date.today()
    months = ['zero', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
              'novembre', 'décembre']
    return months[today.month]


def get_amount(type, zone):
    zone_view = VirtualZoneTotal.objects.get(relevant_model=zone.id)
    if type == "FOUNTAIN":
        return zone_view.fountains
    elif type == 'KIOSK':
        return zone_view.kiosks
    elif type == "INDIVIDUAL":
        return zone_view.indiv_outputs
    elif type == "PIPE":
        return zone_view.pipes
    elif type == "TANK":
        return zone_view.tanks
    else:
        return 0


def get_amount_fountain(zone):
    return get_amount("FOUNTAIN", zone)


def get_amount_kiosk(zone):
    return get_amount("KIOSK", zone)


def get_amount_individual(zone):
    return get_amount("INDIVIDUAL", zone)


def get_amount_pipe(zone):
    return get_amount("PIPE", zone)


def get_amount_household(request):
    if is_user_zone(request):
        zone = request.user.profile.zone
        zone_view = VirtualZoneTotal.objects.get(relevant_model=zone.id)
        return zone_view.indiv_consumers
    elif is_user_fountain(request):
        total = 0
        for outlet in request.user.profile.outlets:
            consumers_outlet = Consumer.objects.filter(water_outlet_id=outlet)
            total += len(consumers_outlet)
        return total


def get_total_consumers(request):
    result = 0
    if is_user_zone(request):
        zone = request.user.profile.zone
        zone_view = VirtualZoneTotal.objects.get(relevant_model=zone.id)
        return zone_view.total_consumers
    elif is_user_fountain(request):
        for outlet in request.user.profile.outlets:
            view = VirtualElementTotal.objects.get(relevant_model=outlet)
            result += view.total_consumers
    return result


def get_amount_indiv_consummer(zone):
    result = 0
    for consumer in Consumer.objects.all():
        if consumer.water_outlet.zone.name in zone.subzones:
            result += consumer.household_size+1
    return result


def get_outlets(request):
    zone = request.user.profile.zone
    outlets = request.user.profile.outlets
    if zone:
        all_outlets = Element.objects.filter(zone__name__in=zone.subzones, type__in=["KIOSK", "FOUNTAIN", "INDIVIDUAL"])
        result = []
        for elem in all_outlets:
            result.append((elem.id, elem.name))
        return result
    else:
        result = []
        for elem_id in outlets:
            elem = Element.objects.get(id=elem_id)
            result.append((elem.id, elem.name))
        return result


def get_outlets_report(request):
    all_outlets = get_outlets(request)
    result = []
    for elem in all_outlets:
        reports = Report.objects.filter(water_outlet=elem[0],
                                        timestamp__month=datetime.date.today().month)
        if len(reports) == 0:
            result.append(elem)
    return result


def get_quantity_distributed(request):
    outlets = get_outlets(request)
    total = 0
    for outlet in outlets:
        report = Report.objects.filter(water_outlet=outlet[0],
                                       timestamp__month=datetime.date.today().month,
                                       has_data=True,
                                       was_active=True)
        if len(report) == 1:
            report = report[0]
            total += report.quantity_distributed
    return [total, round(total*264.17, 3)] #m3, gals


def get_zone(request):
    if is_user_zone(request):
        return request.user.profile.zone.name
    else:
        zone = get_higher_zone(request.user.profile.outlets)
        return zone.name


def get_higher_zone(outlets):
    zone = ""
    for elem in outlets:
        out = Element.objects.filter(id=elem)
        if len(out) == 1:
            out = out[0]
            if zone == "": #First zone found
                zone = out.zone
            elif out.zone.name not in zone.subzones and zone.name in out.zone.subzones: #New zone is higher
                zone = out.zone
    return zone


def has_access(outlet, request):
    if is_user_fountain(request):
        return str(outlet.id) in request.user.profile.outlets
    elif is_user_zone(request):
        return outlet.zone.name in request.user.profile.zone.subzones
