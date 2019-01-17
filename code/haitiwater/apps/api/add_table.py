import re
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from ..log.models import Transaction
from ..water_network.models import Element, ElementType, Zone
from ..consumers.models import Consumer
from ..report.models import Report, Ticket
from django.contrib.auth.models import User, Group
from ..api.get_table import *

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json

success_200 = HttpResponse(status=200)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_consumer_element(request):
    first_name = request.POST.get("firstname", None)
    last_name = request.POST.get("lastname", None)
    gender = request.POST.get("gender", None)
    address = request.POST.get("address", None)
    sub = request.POST.get("subconsumer", None)
    phone = request.POST.get("phone", None)
    outlet_id = request.POST.get("mainOutlet", None)
    outlet = Element.objects.filter(id=outlet_id)
    if len(outlet) > 0:
        outlet = outlet[0]
    else:
        return HttpResponse("La sortie d'eau spécifiée n'a pas été trouvée, impossible " +
                            "d'ajouter le consommateur", status=404)
    new_c = Consumer(last_name=last_name, first_name=first_name,
                          gender=gender, location=address, phone_number=phone,
                          email="", household_size=sub, water_outlet=outlet) #Creation
    transaction = Transaction(user=request.user)
    transaction.save()
    new_c.log_add(transaction)
    new_c.save()
    return success_200

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_network_element(request):
    type = request.POST.get("type", None).upper()
    loc = request.POST.get("localization", None)
    state = request.POST.get("state", None).upper()
    string_type = ElementType[type].value
    zone = request.user.profile.zone
    e = Element(name=string_type+" "+loc, type=type, status=state,
                location=loc, zone=zone) #Creation
    e.save()
    return success_200

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_report_element(request):
    values = json.loads(request.body.decode("utf-8"))
    for index, elem in enumerate(values["selectedOutlets"]):
        outlets = Element.objects.filter(id=elem)
        if len(outlets) < 1:
            return HttpResponse("La sortie d'eau concernée par ce rapport n'a pas été trouvée", status=404)
        else:
            outlet = outlets[0]
        active = values["isActive"]
        meters_distr = values["details"][index]["cubic"]
        value_meter = values["details"][index]["perCubic"]
        month = values["month"]
        year = 2018 #TODO : Temporary
        recette = values["details"][index]["bill"]
        report_line = Report(water_outlet=outlet, was_active=active,
                             quantity_distributed=meters_distr, price=value_meter,
                             month=month, year=year, recette=recette)
        report_line.save()
    return success_200

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_zone_element(request):
    name = request.POST.get("name", None)
    if request.user and request.user.profile.zone: #If user is connected and zone manager
        result = Zone.objects.filter(name=request.user.profile.zone)
        if len(result) == 1:
            super = result[0]
            to_add = Zone(name=name, superzone=super, subzones=[name])
            for z in Zone.objects.all():
                if z.name == super.name: #If the zone is the superZone
                    z.subzones.append(name)
                    z.save()
            to_add.save()
            return success_200
        else:
            return HttpResponse("Impossible de trouver la zone gérée pas l'utilisateur", status=404)
    else:
        return HttpResponse("Impossible d'ajouter la zone. Etes-vous sûr d'être connecté ?", status=500)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_collaborator_element(request):
    first_name = request.POST.get("firstname", None)
    last_name = request.POST.get("lastname", None)
    username = request.POST.get("id", None)
    password = User.objects.make_random_password() #New random password
    email = request.POST.get("email", None)
    new_user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=first_name, last_name=last_name)
    type = request.POST.get("type", None)
    if type == "fountain-manager":
        water_out = request.POST.get("outlets", None)
        print(water_out)
        if len(water_out) < 1:
            return HttpResponse("Vous n'avez pas choisi de fontaine a attribuer !", status=500)
        if len(water_out) > 1:
            res = Element.objects.filter(id__in=water_out)
        else:
            res = Element.objects.filter(id=water_out)
        if len(res) > 0:
            for outlet in res:
                new_user.profile.outlets.append(outlet.id)
        else:
            return HttpResponse("Impossible d'attribuer cette fontaine au gestionnaire", status=404)
        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        my_group.user_set.add(new_user)
    elif type == "zone-manager":
        zone = request.POST.get("zone", None)
        res = Zone.objects.filter(id=zone)
        if len(res) == 1:
            new_user.profile.zone = res[0]
        else:
            return HttpResponse("Impossible d'attribuer cette zone au gestionnaire", status=404)
        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(new_user)
    else:
        new_user.delete()
        return HttpResponse("Impossible d'ajouter l'utilisateur", status=500)
    send_mail(
        'Bienvenue sur haitiwater !',
        'Bienvenue sur haitiwater. Voici votre mot de passe autogénéré : ' + password +
        '\nVeuillez vous connecter pour le modifier.\nPour rappel, ' +
        'votre identifiant est : ' + username,
        '',
        [email],
        fail_silently=False,
    )
    new_user.save()
    return success_200

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_ticket_element(request):
    id = request.POST.get("id_outlet", None)
    outlets = Element.objects.filter(id=id)
    if len(outlets) < 1:
        return HttpResponse("Impossible de trouver la sortie d'eau correspondante au ticket", status=404)
    else:
        outlet = outlets[0]
        typeR = request.POST.get("type", None).upper()
        comment = request.POST.get("comment", None)
        urgency = request.POST.get('urgency', None).upper()
        image = request.FILES.get("picture", None)
        ticket = Ticket(water_outlet=outlet, type=typeR, comment=comment,
                        urgency=urgency, image=image)
        ticket.save()
    return success_200