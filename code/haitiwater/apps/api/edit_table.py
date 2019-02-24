import django
from django.http import HttpResponse

from ..water_network.models import Element, Zone
from ..consumers.models import Consumer
from ..log.models import Transaction, Log
from ..report.models import Ticket
from django.contrib.auth.models import User, Group
from django.db.models import Field


success_200 = HttpResponse(status=200)


def edit_water_element(request):
    id = request.POST.get("id", None)
    elems = Element.objects.filter(id=id)
    if len(elems) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    elem = elems[0]
    old = elem.infos()
    elem.type = request.POST.get("type", None).upper()
    elem.location = request.POST.get("localization", None)
    elem.status = request.POST.get("state", None).upper()
    elem.name = elem.get_type()+" "+elem.location
    log_element(elem, old, request)
    elem.save()
    return success_200


def edit_consumer(request):
    id = request.POST.get("id", None)
    consumers = Consumer.objects.filter(id=id)
    if len(consumers) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    consumer = consumers[0]
    old = consumers[0].infos()
    consumer.first_name = request.POST.get("firstname", None)
    consumer.last_name = request.POST.get("lastname", None)
    consumer.gender = request.POST.get("gender", None)
    consumer.location = request.POST.get("address", None)
    consumer.household_size = request.POST.get("subconsumer", None)
    consumer.phone = request.POST.get("phone", None)
    outlet_id = request.POST.get("mainOutlet", None)
    outlet = Element.objects.filter(id=outlet_id)
    if len(outlet) > 0:
        outlet = outlet[0]
    else:
        return HttpResponse("Impossibe de trouver cet élément du réseau", status=404)  # Outlet not found, can't edit
    consumer.water_outlet = outlet
    log_element(consumer, old, request)
    consumer.save()
    return success_200


def edit_zone(request):
    id = request.POST.get("id", None)
    zone = Zone.objects.filter(id=id)
    if len(zone) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    zone = zone[0]
    old = zone.infos()
    old_name = zone.name
    zone.name = request.POST.get("name", None)
    zone.subzones.remove(old_name)
    zone.subzones.append(zone.name)
    for z in Zone.objects.all():
        if old_name in z.subzones:
            z.subzones.remove(old_name)
            z.subzones.append(zone.name)
            z.save()
    log_element(zone, old, request)
    zone.save()
    return success_200


def edit_ticket(request):
    id = request.POST.get("id", None)
    ticket = Ticket.objects.filter(id=id)
    if len(ticket) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    ticket = ticket[0]
    old = ticket.infos()
    id_outlet = request.POST.get("id_outlet", None)
    outlet = Element.objects.filter(id=id_outlet)
    if len(outlet) != 1:
        return HttpResponse("Impossible de trouver l'élément du réseau associé", status=404)
    outlet = outlet[0]
    ticket.water_outlet = outlet
    ticket.urgency = request.POST.get("urgency", None).upper()
    ticket.type = request.POST.get("type", None).upper()
    ticket.comment = request.POST.get("comment", None)
    ticket.status = request.POST.get("state", None).upper()
    image = request.FILES.get("picture", None)
    if image is not None:
        extension = image.name.split(".")
        import uuid
        filename = str(uuid.uuid4())
        image.name = filename + "." + extension[1]
        ticket.image = image
    log_element(ticket, old, request)
    ticket.save()
    return success_200


def edit_manager(request):
    id = request.POST.get("id", None)
    user = User.objects.filter(username=id)
    if len(user) == 1:
        user = user[0]
        old = user.profile.infos()
        type = request.POST.get("type", None)
        if type == "fountain-manager":
            water_out = request.POST.get("outlets", None)
            water_out = water_out.split(',')
            if len(water_out) > 1:
                res = Element.objects.filter(id__in=water_out)
            else:
                res = Element.objects.filter(id=water_out)
            if len(res) > 0:
                for outlet in res:
                    user.profile.outlets = []
                    user.profile.outlets.append(outlet.id)
            my_group = Group.objects.get(name='Gestionnaire de fontaine')
            my_group.user_set.add(user)
            if user.profile.zone: #If user had a zone, switch it
                g = Group.objects.get(name='Gestionnaire de zone')
                g.user_set.remove(user)
                user.profile.zone = None
            log_element(user.profile, old, request)
            user.save()
        elif type == "zone-manager":
            zone = request.POST.get("zone", None)
            res = Zone.objects.filter(id=zone)
            if len(res) == 1:
                user.profile.zone = res[0]
            else:
                return HttpResponse("Impossible d'assigner cette zone", status=404)
            my_group = Group.objects.get(name='Gestionnaire de zone')
            my_group.user_set.add(user)
            if len(user.profile.outlets) > 0: #If user had outlets
                g = Group.objects.get(name='Gestionnaire de fontaine')
                g.user_set.remove(user)
                user.profile.outlets = []
            log_element(user.profile, old, request)
            user.save()
    else:
        return HttpResponse("Utilisateur introuvable dans la base de donnée",
                          status=404)
    return success_200


def log_element(element, old, request):
    transaction = Transaction(user=request.user)
    transaction.save()
    element.log_edit(old, transaction)
    clean_up(element)


def clean_up(element):
    logs = Log.objects.filter(action="EDIT", column_name="ID", table_name=element._meta.model_name,
                             new_value=element.id)
    if len(logs) != 0:  # If we found a logs modifying this element
        transactions = []
        for log in logs:
            transactions.append(log.transaction)
        all_logs = Log.objects.filter(transaction__in=transactions)
        to_delete = []
        for log_one in all_logs:
            for log_two in all_logs:
                if log_one.transaction.id != log_two.transaction.id:
                    if log_one.column_name == log_two.column_name and log_one.old_value == log_two.new_value:
                        if log_one not in to_delete:
                            to_delete.append(log_one)
                        if log_two not in to_delete:
                            to_delete.append(log_two)
        for elem in to_delete:
            elem.delete()
    for transaction in Transaction.objects.all():
        logs = Log.objects.filter(transaction=transaction)
        if len(logs) == 0:
            transaction.delete()
