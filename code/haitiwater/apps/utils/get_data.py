from ..water_network.models import Element
from ..consumers.models import Consumer
from ..report.models import Report


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


def get_amount_consumer(zone):
    res = 0
    for consumer in Consumer.objects.all():
        if consumer.water_outlet.zone.name in zone.subzones:
            res += 1
    return res


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
        reports = Report.objects.filter(water_outlet=elem.id) #TODO add filter by month
        if len(reports) == 0:
            result.append((elem.id, elem.name))
    return result
