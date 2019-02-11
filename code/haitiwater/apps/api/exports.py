import re

from ..water_network.models import Element, ElementType, Zone
from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from django.contrib.auth.models import User, Group
from ..api.get_table import *
from ..api.add_table import *
from ..api.edit_table import *
from ..utils.get_data import is_user_fountain
from ..log.models import Transaction, Log

import json

error_500 = HttpResponse(False, status=500)
error_404 = HttpResponse(False, status=404)
success_200 = HttpResponse(status=200)


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
    if export_format == "average_monthly_volume_per_zone":
        # Todo backend : fill "label" with list of zones and "data" with their average output volume in cubic meters.
        # Note that they obviously have to be in the same order
        # Note that the conversion and use of galleons is done in front-end
        # For the formula, I think it would be better to differentiate zones with no data and zones with volume = 0. So
        # that "new" zones aren't left behind for lack of data.
        export = """{
                       "jsonarray": [{
                          "label": ["Nom zone 1", "Nome zone 2"],
                          "data": [10, 20]
                       }]}"""
        json_val = json.loads(export)
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
    elif d["table_name"] == "logs":
        all = get_logs_elements(request, json_test, d)
    else:
        return HttpResponse("Impossible de charger la table demande ("+d["table_name"]+").", status=404)
    if all is False: #There was a problem when retrieving the data
        return HttpResponse("Problème à la récupération des données de la table "+d["table_name"], status=500)
    if d["table_name"] == "logs":
        if len(all) > 1:
            keys = list(all[0].keys())
            final = sorted(all, key=lambda x: x[keys[d["column_ordered"]]],
                       reverse=d["type_order"] != "asc")
        else:
            final = all
    else:
        final = sorted(all, key=lambda x: x[d["column_ordered"]],
                       reverse=d["type_order"] != "asc")
    if d["length_max"] == -1:
        json_test["data"] = final
    else:
        json_test["data"] = final[d["start"]:d["start"]+d["length_max"]]
    json_test["recordsFiltered"] = len(final)
    print(json.dumps(json_test))
    return HttpResponse(json.dumps(json_test))


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


def remove_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        id = request.POST.get("id", None)
        consumers = Consumer.objects.filter(water_outlet=id)
        if len(consumers) > 0: #Can't suppress outlets with consummers
            return HttpResponse("Vous ne pouvez pas supprimer cet élément, il est encore attribué à " +
                                "des consommateurs", status=500)
        elem_delete = Element.objects.filter(id=id)
        if len(elem_delete) != 1:
            return HttpResponse("Impossible de supprimer cet élément", status=500)
        elem_delete = elem_delete[0]
        transaction = Transaction(user=request.user)
        transaction.save()
        elem_delete.log_delete(transaction)
        elem_delete.delete()
        tickets = Ticket.objects.filter(water_outlet=id)
        for t in tickets:
            t.log_delete(transaction)
            t.delete()
        users = User.objects.filter()
        for u in users:
            if len(u.profile.outlets) > 0: #Gestionnaire de fontaine
                if str(id) in u.profile.outlets:
                    old = u.profile.infos()
                    u.profile.outlets.remove(str(id))
                    u.save()
                    u.profile.log_edit(old, transaction)
        return success_200
    elif element == "consumer":
        id = request.POST.get("id", None)
        to_delete = Consumer.objects.filter(id=id)
        if len(to_delete) != 1:
            return HttpResponse("Impossible de supprimer cet élément", status=500)
        to_delete = to_delete[0]
        log_element(to_delete, request)
        to_delete.delete()
        return HttpResponse({"draw": request.POST.get("draw", 0)+1}, status=200)
    elif element == "manager":
        id = request.POST.get("id", None)
        to_delete = User.objects.filter(username=id)
        if len(to_delete) != 1:
            return HttpResponse("Impossible de supprimer cet élément", status=500)
        to_delete = to_delete[0]
        log_element(to_delete.profile, request)
        to_delete.delete()
        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)
    elif element == "ticket":
        id = request.POST.get("id", None)
        to_delete = Ticket.objects.filter(id=id)
        if len(to_delete) != 1:
            return HttpResponse("Impossible de supprimer cet élément", status=500)
        to_delete = to_delete[0]
        log_element(to_delete, request)
        to_delete.delete()
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
        transaction = Transaction(user=request.user)
        transaction.save()
        for z in Zone.objects.all():
            if str(id) in z.subzones:
                old = z.infos()
                z.subzones.remove(str(id))
                z.save()
                z.log_edit(old, transaction)
        to_delete.log_delete(transaction)
        to_delete.delete()
        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)
    return error_500


def edit_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        return edit_water_element(request)
    elif element == "consumer":
        return edit_consumer(request)
    elif element == "zone":
        return edit_zone(request)
    elif element == "ticket":
        return edit_ticket(request)
    elif element == "manager":
        return edit_manager(request)
    else:
        return HttpResponse("Impossible d'éditer la table "+element+
                            ", elle n'est pas reconnue", status=500)

def roll_back(transaction):
    logs = Log.objects.filter(transaction=transaction)
    if logs[0].action == "EDIT": #Edit case
        elements = get_elem_logged(logs)
        tables = []
        for log in logs:
            if log.column_name == "id":
                tables.append(log.table_name)
        for number, table in enumerate(tables):
            roll_back_item(elements[number], {log.column_name: log.old_value
                       for log in logs
                       if log.table_name == table and log.column_name != "id"})

        for log in logs:
            log.delete()
        transaction.delete()
    elif logs[0].action == "ADD": #Add case
        elements = get_elem_logged(logs)
        for elem in elements:
            elem.delete()
        for log in logs:
            log.delete()
        transaction.delete()
    elif logs[0].action == "DELETE": #Delete case
        re_add_item(logs)
        for log in logs:
            log.delete()
        transaction.delete()

def roll_back_item(item, values):
    for field, value in values.items():
        item.__setattr__(field, value)
    item.save()


def re_add_item(logs):
    tables = []
    for log in logs:
        if log.column_name == "id":
            tables.append(log.table_name)
    for table in tables:
        restore_item({log.column_name: log.old_value
                       for log in logs
                       if log.table_name == table and log.column_name != "id"},
                      table)

def restore_item(dict, table):
    if table == "Consumer":
        outlet = Element.objects.filter(id=dict["water_outlet"])
        if len(outlet) != 1:
            return HttpResponse("Impossible de restaurer cet élément", status=500)
        outlet = outlet[0]
        restored = Consumer(last_name=dict["last_name"], first_name=dict["first_name"],
                          gender=dict["gender"], location=dict["location"], phone_number=dict["phone_number"],
                          email="", household_size=dict["household_size"], water_outlet=outlet)
        restored.save()
    elif table == "Ticket":
        outlet = Element.objects.filter(id=dict["water_outlet"])
        if len(outlet) != 1:
            return HttpResponse("Impossible de restaurer cet élément", status=500)
        outlet = outlet[0]
        restored = Ticket(water_outlet=outlet, type=dict["type"],
                          comment=dict["comment"], urgency=dict["urgency"], image=None)
        restored.save()
    elif table == "WaterElement":
        zone = Zone.objects.filter(id=dict["zone"])
        if len(zone) != 1:
            return HttpResponse("Impossible de restaurer cet élément", status=500)
        zone = zone[0]
        restored = Element(name=dict["name"], type=dict["type"],
                           status=dict["status"], location=dict["location"],
                           zone=zone)
        restored.save()
    elif table == "Zone":
        super_zone = Zone.objects.filter(id=dict["superzone"])
        if len(super_zone) != 1:
            return HttpResponse("Impossible de restaurer cet élément", status=500)
        super_zone = super_zone[0]
        restored = Zone(name=dict["name"], superzone=super_zone, subzones=[dict["name"]])
        up = True
        while up:
            super_zone.subzones.append(dict["name"])
            super_zone.save()
            super_zone = super_zone.superzone
            if super_zone == None:
                up = False
        restored.save()
    elif table == "Report":
        pass
    elif table == "User":
        password = User.objects.make_random_password()  # New random password
        user = User.objects.create_user(username=dict["identifiant"],
                                        email=dict["email"],
                                        password=password,
                                        first_name=dict["first_name"],
                                        last_name=dict["last_name"])

        if dict["role"] == "Gestionnaire de fontaine":
            water_out = dict["outlets"]
            if len(water_out) < 1:
                return HttpResponse("Vous n'avez pas choisi de fontaine a attribuer !", status=500)
            if len(water_out) > 1:
                res = Element.objects.filter(id__in=water_out)
            else:
                res = Element.objects.filter(id=water_out)
            if len(res) > 0:
                for outlet in res:
                    user.profile.outlets.append(outlet.id)
            else:
                return HttpResponse("Impossible d'attribuer cette fontaine au gestionnaire", status=404)
            my_group = Group.objects.get(name='Gestionnaire de fontaine')
            my_group.user_set.add(user)
        elif dict["role"] == "Gestionnaire de zone":
            zone = dict["zone"]
            res = Zone.objects.filter(id=zone)
            if len(res) == 1:
                user.profile.zone = res[0]
            else:
                return HttpResponse("Impossible d'attribuer cette zone au gestionnaire", status=404)
            my_group = Group.objects.get(name='Gestionnaire de zone')
            my_group.user_set.add(user)
        else:
            user.delete()
            return HttpResponse("Impossible d'ajouter l'utilisateur", status=500)
        send_mail(
            'Changement de mot de passe.',
            'Votre compte haitiwater a été modifié, vous devez donc en changer le mot de passe.'+
            '\nVoici votre nouveau mot de passe autogénéré : ' + password +
            '\nVeuillez vous connecter pour le modifier.\nPour rappel, ' +
            'votre identifiant est : ' + dict["identifiant"],
            '',
            [dict["email"]],
            fail_silently=False,
        )

def get_elem_logged(logs):
    ids = []
    tables = []
    for elem in logs:
        if elem.column_name =="id":
            ids.append(elem.new_value)
            tables.append(elem.table_name)
    elems = []
    for number, table in enumerate(tables):
        elem = None
        if table == "Consumer":
            elem = Consumer.objects.filter(id=ids[number])[0]
        elif table == "Ticket":
            elem = Ticket.objects.filter(id=ids[number])[0]
        elif table == "WaterElement":
            elem = Element.objects.filter(id=ids[number])[0]
        elif table == "Zone":
            elem = Zone.objects.filter(id=ids[number])[0]
        elif table == "Report":
            elem = Report.objects.filter(id=ids[number])[0]
        elif table == "User":
            elem = User.objects.filter(id=ids[number])[0]
        elems.append(elem)
    return elems

def log_element(element, request):
    transaction = Transaction(user=request.user)
    transaction.save()
    element.log_delete(transaction)


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
