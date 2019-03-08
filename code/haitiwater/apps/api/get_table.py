import json
from decimal import Decimal, ROUND_HALF_UP

from django.http import HttpResponse
from django.contrib.auth.models import User, Group

from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from ..water_network.models import Element, Zone
from ..financial.models import Invoice, Payment
from ..utils.get_data import is_user_fountain, is_user_zone
from ..log.models import Transaction, Log


def filter_search(parsed, values):
    result = []
    if parsed["search"] == "" and len(values) > 0:
        for elem in values:
            result.append(elem)
    else:
        for elem in values:
            for cols in parsed["searchable"]:
                if cols < len(elem) and parsed["search"].lower() in str(elem[cols]).lower():
                    result.append(elem)
                    break
    return result


def get_water_elements(request, json, parsed):
    zone = request.user.profile.zone
    outlets = request.user.profile.outlets
    if zone: #If there is a zone, we have a zone manager
        target = Zone.objects.filter(name=zone.name)
        if len(target) == 1:
            target = target[0]
        else:
            return False
        all_water_element = Element.objects.filter(zone__name__in=target.subzones)
    else: #We have a fountain manager
        all_water_element =Element.objects.filter(id__in=outlets)
    json["recordsTotal"] = len(all_water_element)
    all = []
    for elem in all_water_element:
        tab = elem.network_descript()
        all.append(tab)
    return all


def get_consumer_elements(request, json, parsed):
    all_consumers = None
    if is_user_zone(request):
        zone_id = request.GET.get("zone", None)  # TODO check if user can access this zone
        zone = Zone.objects.get(id=zone_id) if zone_id else request.user.profile.zone
        all_consumers = [elem for elem in Consumer.objects.all() if elem.water_outlet.is_in_subzones(zone)]
    elif is_user_fountain(request):
        outlets = request.user.profile.outlets
        all_consumers = Consumer.objects.filter(water_outlet_id__in=outlets)

    result = []
    json["recordsTotal"] = len(all_consumers)
    for elem in all_consumers:
        result.append(elem.descript())
    return result


def get_zone_elements(request, json, parsed):
    all = []
    if request.user.profile.zone: #Zone manager
        for z in request.user.profile.zone.subzones:
            zone = Zone.objects.filter(name=z)
            if len(zone) == 1:
                all.append(zone[0].descript())

        json["recordsTotal"] = len(all)
    return all


def get_manager_elements(request, json, parsed):
    all = []
    if request.user.profile.zone:#Zone manager
        zone = request.user.profile.zone
        target = Zone.objects.filter(name=zone.name)
        if len(target) == 1:
            target = target[0]
        else:
            return False
        all_collab = User.objects.all()
        for u in all_collab:
            group = u.groups.values_list('name', flat=True)
            if "Gestionnaire de zone" in group:
                if type(target) is Zone and u.profile.zone and \
                                u.profile.zone.name in target.subzones:
                    tab = [u.username, u.last_name, u.first_name, u.email,
                           "Gestionnaire de zone", u.profile.zone.name,
                           u.profile.outlets]
                    all.append(tab)
            if "Gestionnaire de fontaine" in group:
                for elem in u.profile.outlets:
                    out = Element.objects.filter(id=elem)
                    if len(out) == 1:
                        out = out[0]
                    if type(out) is Element and out.is_in_subzones(target):
                        tab = [u.username, u.last_name, u.first_name, u.email,
                               "Gestionnaire de fontaine", u.profile.get_zone(),
                               u.profile.outlets]
                        all.append(tab)
                        break
        json["recordsTotal"] = len(all)
    return all


def get_ticket_elements(request, json, parsed):
    all = []
    if request.user.profile.zone: #Zone manager
        for elem in Ticket.objects.all():
            if elem.water_outlet.zone.name in request.user.profile.zone.subzones:
                all.append(elem.descript())
    else: #Fountain manager
        for elem in Ticket.objects.all():
            if str(elem.water_outlet.id) in request.user.profile.outlets:
                all.append(elem.descript())
        json["recordsTotal"] = len(all)
    return all


def get_last_reports(request, json, parsed):
    from ..utils.get_data import is_user_fountain
    all_reports = []
    all = []
    if is_user_fountain(request):
        for outlet_id in request.user.profile.outlets:
            outlet = Element.objects.get(id=outlet_id)
            if outlet:
                reports = Report.objects.filter(water_outlet=outlet).order_by("timestamp")[:5]
                for report in reports:
                    all_reports.append(report)
    else:
        pass
    for report in all_reports:
        detail = {"id": report.water_outlet_id,
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
        for elem in all:
            if str(report.timestamp.date().month) in elem["date"]:
                elem["details"].append(detail)
                new = False
        if new:
            infos =  {"id": report.id,
                 "date": str(report.timestamp.date()),
                 "details":[detail]
                }
            all.append(infos)
    json["recordsTotal"] = len(all)
    return all


def get_logs_elements(request, json, parsed):
    transactions = Transaction.objects.filter(user__in=request.user.profile.get_subordinates())
    all = []
    for t in transactions:
        logs = Log.objects.filter(transaction=t)
        details = get_transaction_detail(logs)
        item = {"id": t.id, "time": str(t.timestamp.date()),
                "type": logs[0].get_action(), "user": t.user.username,
                "summary": logs[0].get_table(), "details": details}
        all.append(item)
    json["recordsTotal"] = len(all)
    return all

def get_transaction_detail(logs):
    detail = ""
    for indiv in logs:
        if indiv.action == "ADD":
            if indiv.new_value and indiv.new_value != "[]":
                detail += indiv.column_name+" : "+indiv.new_value + "<br>"
        elif indiv.action == "DELETE":
            if indiv.old_value and indiv.old_value != "[]":
                detail += indiv.column_name+" : "+indiv.old_value + "<br>"
        else:
            if indiv.old_value and indiv.new_value:
                if indiv.column_name == "ID":
                    detail += "Id : " + indiv.old_value
                else:
                    detail += indiv.column_name+" : "+indiv.old_value +" -> "+\
                          indiv.new_value+"<br>"
    return detail


def get_payment_elements(request, json, parsed, id):
    all = []
    for elem in Payment.objects.filter(consumer_id=id):
        all.append(elem.descript())
    json["recordsTotal"] = len(all)
    return all


def get_payment_details(request):
    id = request.GET.get("id", None)
    balance = 0
    validity = None
    for elem in Invoice.objects.filter(consumer_id=id):
        balance -= elem.amount
        if not validity or elem.expiration > validity:
            validity = elem.expiration
    for elem in Payment.objects.filter(consumer_id=id):
        balance += elem.amount
    return balance, str(validity)
