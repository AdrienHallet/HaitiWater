import re
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from ..log.models import Transaction
from ..water_network.models import Element, ElementType, Zone
from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from django.contrib.auth.models import User, Group


success_200 = HttpResponse(status=200)

def edit_water_element(request):
    id = request.POST.get("id", None)
    elems = Element.objects.filter(id=id)
    if len(elems) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    elem = elems[0]
    elem.type = request.POST.get("type", None).upper()
    elem.location = request.POST.get("localization", None)
    elem.status = request.POST.get("state", None).upper()
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
    transaction = Transaction(user=request.user)
    transaction.save()
    print("Allo ?")
    consumer.log_edit(old, transaction)
    consumer.save()
    return success_200


def edit_zone(request):
    id = request.POST.get("id", None)
    zone = Zone.objects.filter(id=id)
    if len(zone) < 1:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=404)
    zone = zone[0]
    old_name = zone.name
    zone.name = request.POST.get("name", None)
    zone.subzones.remove(old_name)
    zone.subzones.append(zone.name)
    for z in Zone.objects.all():
        if old_name in z.subzones:
            z.subzones.remove(old_name)
            z.subzones.append(zone.name)
            z.save()
    zone.save()
    return success_200


def edit_manager(request):
    id = request.POST.get("id", None)
    user = User.objects.filter(username=id)
    if len(user) == 1:
        user = user[0]
        type = request.POST.get("type", None)
        if type == "fountain-manager":
            water_out = request.POST.get("outlets", None)
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
            user.save()
    else:
        return HttpResponse("Utilisateur introuvable dans la base de donnée",
                          status=404)
    return success_200
