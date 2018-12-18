import json

from django.http import HttpResponse

from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from ..water_network.models import Element, Zone
from django.contrib.auth.models import User, Group


def get_water_elements(request, json, parsed):
    all = []
    zone = request.user.profile.zone
    if zone:
        target = Zone.objects.filter(name=zone.name)[0]
        all_water_element = [elem for elem in Element.objects.all() if elem.is_in_subzones(target)]
        json["recordsTotal"] = len(all_water_element)
        for elem in all_water_element:
            cust = Consumer.objects.filter(water_outlet=elem)
            distributed = Report.objects.filter(water_outlet=elem)
            quantity = 0
            for report in distributed:
                quantity += report.quantity_distributed
            tab = elem.network_descript()
            tab.insert(4, quantity)
            tab.insert(5, quantity * 219.969)  # TODO make sure this is correct
            tab.insert(3, len(cust))
            if parsed["search"] == "":
                all.append(tab)
            else:
                for cols in parsed["searchable"]:
                    if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                        all.append(tab)
                        break
    return all


def get_consumer_elements(request, json, parsed):
    all = []
    zone = request.user.profile.zone
    if zone:
        target = Zone.objects.filter(name=zone.name)[0]
        all_consumers = [elem for elem in Consumer.objects.all() if elem.water_outlet.is_in_subzones(target)]
        json["recordsTotal"] = len(all_consumers)
        for elem in all_consumers:
            if parsed["search"] == "":
                all.append(elem.descript())
            else:
                for cols in parsed["searchable"]:
                    tab = elem.descript()
                    if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                        all.append(tab)
                        break
    return all


def get_zone_elements(request, json, parsed):
    all = []
    if request.user.profile.zone:
        json["recordsTotal"] = len(request.user.profile.zone.subzones)
        for z in request.user.profile.zone.subzones:
            zone = Zone.objects.filter(name=z)
            if len(zone) == 1:
                if parsed["search"] == "":
                    all.append(zone[0].descript())
                else:
                    for cols in parsed["searchable"]:
                        tab = zone[0].descript()
                        if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                            all.append(tab)
                            break
    return all


def get_manager_elements(request, json, parsed):
    all = []
    if request.user.profile.zone:
        zone = request.user.profile.zone
        target = Zone.objects.filter(name=zone.name)[0]
        all_collab = User.objects.all()
        json["recordsTotal"] = len(all_collab) -1 #Remove the admin account
        for u in all_collab:
            group = u.groups.values_list('name', flat=True)
            if "Gestionnaire de zone" in group:
                if u.profile.zone.name in target.subzones:
                    tab = [u.id, u.last_name, u.first_name, u.email,
                           "Gestionnaire de zone", u.profile.zone.name]
                    if parsed["search"] == "":
                        all.append(tab)
                    else:
                        for cols in parsed["searchable"]:
                            if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                                all.append(tab)
                                break
            if "Gestionnaire de fontaine" in group:
                for elem in u.profile.outlets:
                    out = Element.objects.filter(id=elem)[0]
                    if out.is_in_subzones(target):
                        tab = [u.id, u.last_name, u.first_name, u.email,
                               "Gestionnaire de fontaine", ""]
                        if parsed["search"] == "":
                            all.append(tab)
                        else:
                            for cols in parsed["searchable"]:
                                if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                                    all.append(tab)
                                    break

    return all


def get_ticket_elements(request, json, parsed):
    all = []
    if request.user.profile.zone:
        for elem in Ticket.objects.all():
            if elem.water_outlet.zone.name in request.user.profile.zone.subzones:
                if parsed["search"] == "":
                    all.append(elem.descript())
                else:
                    for cols in parsed["searchable"]:
                        tab = elem.descript()
                        if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                            all.append(tab)
                            break
    else:
        tot = 0
        for elem in Ticket.objects.all():
            if str(elem.water_outlet.id) in request.user.profile.outlets:
                tot += 1
                if parsed["search"] == "":
                    all.append(elem.descript())
                else:
                    for cols in parsed["searchable"]:
                        tab = elem.descript()
                        if cols < len(tab) and parsed["search"].lower() in str(tab[cols]).lower():
                            all.append(tab)
                            break
    json["recordsTotal"] = tot
    return all
