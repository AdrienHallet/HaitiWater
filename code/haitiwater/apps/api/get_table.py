import json

from django.http import HttpResponse

from ..consumers.models import Consumer
from ..report.models import Report
from ..water_network.models import Element, ElementType, Zone

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
