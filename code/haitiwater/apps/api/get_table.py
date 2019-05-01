import json

from django.contrib.auth.models import User
from django.http import HttpResponse

from ..consumers.models import Consumer
from ..financial.models import Invoice, Payment
from ..log.models import Transaction, Log
from ..report.models import Report, Ticket
from ..utils.get_data import is_user_fountain, is_user_zone
from ..water_network.models import Element, Zone, Location


def filter_search(params, values):
    result = []
    for elem in values:
        if params["search"] != "":
            for cols in params["searchable"]:
                if cols < len(elem) and params["search"].lower() in str(elem[cols]).lower():
                    result.append(elem)
                    break
        else:
            result.append(elem)
    return result


def get_water_elements(request):
    elements = []
    if is_user_zone(request):
        elements = Element.objects.filter(zone__name__in=request.user.profile.zone.subzones)
    elif is_user_fountain(request):
        elements = Element.objects.filter(id__in=request.user.profile.outlets)

    result = []
    for element in elements:
        result.append(element.network_descript())

    return result


def get_consumer_elements(request):
    consumers = []
    if is_user_zone(request):
        consumers = Consumer.objects.filter(water_outlet__zone__name__in=request.user.profile.zone.subzones)
    elif is_user_fountain(request):
        consumers = Consumer.objects.filter(water_outlet_id__in=request.user.profile.outlets)

    result = []
    for elem in consumers:
        result.append(elem.descript())

    return result


def get_zone_elements(request):
    result = []

    for zone in Zone.objects.filter(name__in=request.user.profile.zone.subzones):
        result.append(zone.descript())

    return result


def get_manager_elements(request):
    result = []
    zone = request.user.profile.zone

    for user in User.objects.all():  # TODO optimize
        group = user.groups.values_list('name', flat=True)
        if 'Gestionnaire de zone' in group:
            if type(zone) is Zone and user.profile.zone and \
                    user.profile.zone.name in zone.subzones:  # TODO clean
                tab = [user.username, user.last_name, user.first_name, user.profile.get_phone_number(),
                       user.email, "Gestionnaire de zone", user.profile.zone.name, user.profile.outlets]
                result.append(tab)
        if "Gestionnaire de fontaine" in group:
            for elem in user.profile.outlets:
                out = Element.objects.filter(id=elem)
                if len(out) == 1:
                    out = out[0]
                if type(out) is Element and out.is_in_subzones(zone):
                    tab = [user.username, user.last_name, user.first_name, user.profile.get_phone_number(),
                           user.email, "Gestionnaire de fontaine", user.profile.get_zone(), user.profile.outlets]
                    result.append(tab)
                    break

    return result


def get_ticket_elements(request):
    result = []
    if is_user_zone(request):
        for elem in Ticket.objects.filter(water_outlet__zone__name__in=request.user.profile.zone.subzones):
            result.append(elem.descript())
    elif is_user_fountain(request):
        for elem in Ticket.objects.filter(water_outlet_id__in=request.user.profile.outlets):
            result.append(elem.descript())

    return result


def get_last_reports(request):
    all_reports = []
    for outlet in Element.objects.filter(id__in=request.user.profile.outlets):
        reports = Report.objects.filter(water_outlet=outlet).order_by("timestamp")[:5]
        for report in reports:
            all_reports.append(report)

    result = []
    for report in all_reports:
        detail = {
            "id": report.water_outlet_id,
            "name": report.water_outlet.name,
            "has_data": report.has_data,
            "was_active": report.was_active,
            "days_active": report.days_active,
            "hours_active": report.hours_active,
            "volume": report.quantity_distributed,
            "price": report.price,
            "revenue": report.recette
        }
        new = True
        for elem in result:
            if str(report.timestamp.date().month) in elem["date"]:
                elem["details"].append(detail)
                new = False
        if new:
            infos = {
                "id": report.id,
                "date": str(report.timestamp.date()),
                "details": [detail]
            }
            result.append(infos)

    return result


def get_logs_elements(request, archived):
    result = []
    for transaction in Transaction.objects.filter(user__in=request.user.profile.get_subordinates(), archived=archived):
        logs = Log.objects.filter(transaction=transaction)
        details = get_transaction_detail(logs)
        item = {
            "id": transaction.id,
            "time": str(transaction.timestamp.date()),
            "type": logs[0].get_action(),
            "user": transaction.user.username,
            "summary": logs[0].get_table(),
            "details": details
        }
        if archived:
            item["action"] = transaction.get_action()
        result.append(item)

    return result


def get_transaction_detail(logs):
    detail = ""
    for indiv in logs:
        if indiv.action == "ADD":
            if indiv.new_value and indiv.new_value != "[]" and "_" not in indiv.column_name:
                detail += indiv.column_name + " : " + indiv.new_value + "<br>"
        elif indiv.action == "DELETE" and "_" not in indiv.column_name:
            if indiv.old_value and indiv.old_value != "[]":
                detail += indiv.column_name + " : " + indiv.old_value + "<br>"
        else:
            if indiv.old_value and indiv.new_value and "_" not in indiv.column_name:
                if indiv.column_name == "ID":
                    detail += "Id : " + indiv.old_value + "<br>"
                else:
                    detail += indiv.column_name + " : " + indiv.old_value + " -> " + indiv.new_value + "<br>"
    return detail


def get_payment_elements(request):
    consumer_id = request.GET.get("user", "none")
    if consumer_id == "none":
        return None

    result = []
    for elem in Payment.objects.filter(consumer_id=consumer_id):
        result.append(elem.descript())

    return result


def get_payment_details(request):
    consumer_id = request.GET.get("id", None)
    consumer = Consumer.objects.filter(id=consumer_id).first()
    if consumer is None:
        return None

    balance = consumer.get_balance()
    invoice = Invoice.objects.filter(consumer_id=consumer_id).order_by('-expiration').first()
    validity = str(invoice.expiration) if invoice is not None else "Pas de prochaine facturation"

    return balance, validity


def get_details_network(request):
    id_outlet = request.GET.get("id", None)
    outlet = Element.objects.filter(id=id_outlet).first()
    if outlet is None:
        return HttpResponse("Impossible de charger cet élément", status=400)

    location = Location.objects.filter(elem=id_outlet).first()
    if location is not None:
        location = location.json_representation

    infos = {
        "id": id_outlet,
        "type": outlet.get_type(),
        "localization": outlet.location,
        "manager": outlet.manager_names,
        "users": outlet.get_consumers(),
        "state": outlet.get_status(),
        "currentMonthCubic": outlet.get_current_output(),
        "averageMonthCubic": outlet.get_all_output()[1],
        "totalCubic": outlet.get_all_output()[0],
        "geoJSON": location
    }

    return HttpResponse(json.dumps(infos))
