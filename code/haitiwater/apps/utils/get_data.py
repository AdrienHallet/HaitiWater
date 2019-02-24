from ..water_network.models import Element
from ..consumers.models import Consumer
from ..report.models import Report
import datetime


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
    result = 0
    for elem in Element.objects.filter(type=type):
        if elem.zone.name in zone.subzones:
            result += 1
    return result


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
        return get_amount_consumer(zone)
    elif is_user_fountain(request):
        total = 0
        for outlet in request.user.profile.outlets:
            consumers_outlet = Consumer.objects.filter(water_outlet_id=outlet)
            total += len(consumers_outlet)
        return total


def get_amount_consumer(zone):
    res = 0
    for consumer in Consumer.objects.all():
        if consumer.water_outlet.zone.name in zone.subzones:
            res += 1
    return res


def get_total_consumers(request):
    result = 0
    if is_user_zone(request):
        zone = request.user.profile.zone
        for consumer in Consumer.objects.all():
            if consumer.water_outlet.zone.name in zone.subzones:
                result += consumer.household_size + 1
    elif is_user_fountain(request):
        for outlet in request.user.profile.outlets:
            consumers_outlet = Consumer.objects.filter(water_outlet_id=outlet)
            for consumer in consumers_outlet:
                result += consumer.household_size+1
    return result


def get_amount_indiv_consummer(zone):
    result = 0
    for consumer in Consumer.objects.all():
        if consumer.water_outlet.zone.name in zone.subzones:
            result += consumer.household_size
    return result


def get_outlets(request):
    zone = request.user.profile.zone
    outlets = request.user.profile.outlets
    if zone:
        all_outlets = Element.objects.all()
        result = []
        for elem in all_outlets:
            if elem.type in ["KIOSK", "FOUNTAIN", "INDIVIDUAL"] and elem.zone.name in zone.subzones:
                result.append((elem.id, elem.name))
        return result
    else:
        all_outlets = Element.objects.all()
        result = []
        for elem in all_outlets:
            if elem.type in ["KIOSK", "FOUNTAIN", "INDIVIDUAL"] and str(elem.id) in outlets:
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
                                       timestamp__month=datetime.date.today().month)
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
