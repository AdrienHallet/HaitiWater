import re
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from ..water_network.models import Element, ElementType, Zone
from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from django.contrib.auth.models import User, Group
from ..api.get_table import *
from ..api.add_table import *
from ..api.edit_table import *

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json

error_500 = HttpResponse(False, status=500)
error_404 = HttpResponse(False, status=404)
success_200 = HttpResponse(status=200)


def is_user_fountain(request):
    groups = request.user.groups.values_list('name', flat=True)
    return "Gestionnaire de fontaine" in groups


def is_user_zone(request):
    groups = request.user.groups.values_list('name', flat=True)
    return "Gestionnaire de zone" in groups


def graph(request):
    export_format = request.GET.get('type', None)
    if export_format == "consumer_gender_pie":
        export = """{
               "jsonarray": [{
                  "label": "Femmes",
                  "data": 0
               }, {
                  "label": "Hommes",
                  "data": 0
               }, {
                  "label": "Autre",
                  "data": 0
               }]}"""
        json_val = json.loads(export)
        all_consumers = Consumer.objects.all()
        for elem in all_consumers:
            if elem.gender == "F" or elem.gender == "Femme":
                json_val['jsonarray'][0]['data'] += 1 #One more women
            elif elem.gender == "M" or elem.gender == "Homme":
                json_val['jsonarray'][1]['data'] += 1 #One more man
            else:
                json_val['jsonarray'][2]['data'] += 1 #One more other
    return HttpResponse(json.dumps(json_val))


def table(request):
    # Todo backend https://datatables.net/manual/server-side
    # Note that "editable" is a custom field. Setting it to true displays the edit/delete buttons.
    export = """{
                      "editable": true,
                      "data": []
                    }"""
    json_test = json.loads(export)
    json_test["draw"] = str(int(request.GET.get('draw', "1")) + 1)
    d = parse(request)
    print(d)
    all = []
    if d["table_name"] == "water_element":
        if is_user_fountain(request):
            json_test["editable"] = False
        all = get_water_elements(request, json_test, d)
    elif d["table_name"] == "consumer":
        all = get_consumer_elements(request, json_test, d)
    elif d["table_name"] == "zone":
        if is_user_fountain(request):
            return HttpResponse("Vous ne pouvez pas accéder à ces informations", 500)
        all = get_zone_elements(request, json_test, d)
    elif d["table_name"] == "manager":
        if is_user_fountain(request):
            return HttpResponse("Vous ne pouvez pas accéder à ces informations", 500)
        all = get_manager_elements(request, json_test, d)
    elif d["table_name"] == "ticket":
        all = get_ticket_elements(request, json_test, d)
    if all is False: #There was a problem when retrieving the data
        return HttpResponse("Problème à la récupération des données de la table "+d["table_name"], status=500)
    final = sorted(all, key=lambda x: x[d["column_ordered"]],
                   reverse=d["type_order"] != "asc")
    if d["length_max"] == -1:
        json_test["data"] = final
    else:
        json_test["data"] = final[d["start"]:d["start"]+d["length_max"]]
    json_test["recordsFiltered"] = len(final)
    print(json.dumps(json_test))
    return HttpResponse(json.dumps(json_test))

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        return add_network_element(request)
    elif element == "consumer":
        return add_consumer_element(request)
    elif element == "zone":
        return add_zone_element(request)
    elif element == "manager":
        return add_collaborator_element(request)
    elif element == "ticket":
        return add_ticket_element(request)
    else:
        return HttpResponse("Impossible d'ajouter l'élément "+element, status=500)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def remove_element(request):
    print(request.POST)
    element = request.POST.get("table", None)
    if element == "water_element":
        id = request.POST.get("id", None)
        consumers = Consumer.objects.filter(water_outlet=id)
        if len(consumers) > 0: #Can't suppress outlets with consummers
            return HttpResponse("Vous ne pouvez pas supprimer cet élément, il est encore attribué à" +
                                "des consommateurs", status=500)
        Element.objects.filter(id=id).delete()
        tickets = Ticket.objects.filter(water_outlet=id)
        for t in tickets:
            t.delete()
        users = User.objects.filter()
        for u in users:
            if len(u.profile.outlets) > 0: #Gestionnaire de fontaine
                if str(id) in u.profile.outlets:
                    u.profile.outlets.remove(str(id))
                    u.save()
        return success_200
    elif element == "consumer":
        id = request.POST.get("id", None)
        Consumer.objects.filter(id=id).delete()
        return HttpResponse({"draw": request.POST.get("draw", 0)+1}, status=200)
    elif element == "manager":
        id = request.POST.get("id", None)
        User.objects.filter(username=id).delete()
        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)
    elif element == "ticket":
        id = request.POST.get("id", None)
        Ticket.objects.filter(id=id).delete()
        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)
    elif element == "zone":
        id = request.POST.get("id", None)
        to_delete = Zone.objects.filter(id=id)
        if len(to_delete) == 1:
            to_delete = to_delete[0]
        else:
            return HttpResponse("Impossible de trouver la zone que vous essayez de supprimer."+
                                " Essayez de recharger la page.", status=404)
        if len(to_delete.subzones) > 1:
            return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle contient encore" +
                                "d'autres zones", status=500)
        if len(Element.objects.filter(zone=id)) > 0:
            return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle contient encore" +
                                "des élements du réseau", status=500)
        for u in User.objects.all():
            if u.profile.zone == to_delete:
                return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle est encore attribuée à" +
                                "un gestionnaire de zone", status=500)
        for z in Zone.objects.all():
            if str(id) in z.subzones:
                z.subzones.remove(str(id))
                z.save()
        to_delete.delete()
        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)
    return error_500

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def edit_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        return edit_water_element(request)
    elif element == "consumer":
        return edit_consumer(request)
    elif element == "zone":
        return edit_zone(request)
    elif element == "manager":
        return edit_manager(request)
    else:
        return HttpResponse("Impossible d'éditer la table "+element+
                            ", elle n'est pas reconnue", status=500)


def parse(request):
    test1 = re.compile('order\[\d*\]\[column\]')
    test2 = re.compile('order\[\d*\]\[dir\]')
    res1 = list(filter(test1.match, dict(request.GET).keys()))
    res2 = list(filter(test2.match, dict(request.GET).keys()))
    searchable_cols = []
    for i in range(25):
        if request.GET.get('columns['+str(i)+'][searchable]', False):
            searchable_cols.append(i)
    d = {"table_name": request.GET.get('name', None),
         "length_max": int(request.GET.get('length', 10)),
         "start": int(request.GET.get('start', 0)),
         "column_ordered": int(request.GET.get(res1[0], 0)),
         "type_order": request.GET.get(res2[0], 'asc'),
         "search": request.GET.get('search[value]', ""),
         "searchable": searchable_cols
         }

    return d
