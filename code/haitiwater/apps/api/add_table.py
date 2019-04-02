from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group
from django.contrib.gis.geos import GEOSGeometry
from django.core.mail import send_mail

from ..api.get_table import *
from ..utils.get_data import has_access, is_int, is_float
from ..water_network.models import ElementType


def log_element(elem, request):
    transaction = Transaction(user=request.user)
    transaction.save()
    elem.save()
    elem.log_add(transaction)


def add_consumer_element(request):
    first_name = request.POST.get("firstname", None)
    last_name = request.POST.get("lastname", None)
    gender = request.POST.get("gender", None)
    address = request.POST.get("address", None)
    sub = request.POST.get("subconsumer", None)
    phone = request.POST.get("phone", None)
    outlet_id = request.POST.get("mainOutlet", None)

    if not is_int(sub):
        return HttpResponse("Impossible, certains champs devraient être des entiers", status=400)

    outlet = Element.objects.filter(id=outlet_id).first()
    if outlet is None:
        return HttpResponse("La sortie d'eau spécifiée n'a pas été trouvée, "
                            "impossible d'ajouter le consommateur", status=400)

    if not has_access(outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

    consumer = Consumer(last_name=last_name, first_name=first_name, gender=gender, location=address,
                        phone_number=phone, household_size=sub, water_outlet=outlet)  # Creation

    log_element(consumer, request)

    if outlet.type != ElementType.INDIVIDUAL.name:
        price, duration = outlet.get_price_and_duration()
        creation = date.today()
        expiration = creation + relativedelta(months=duration)
        invoice = Invoice(consumer=consumer, water_outlet=outlet, amount=price,
                          creation=creation, expiration=expiration)
        invoice.save()

    return HttpResponse(consumer.id, status=200)


def add_network_element(request):
    if request.user.profile.zone is None:
        return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

    type = request.POST.get("type", None).upper()
    loc = request.POST.get("localization", None)
    state = request.POST.get("state", None).upper()
    name = ElementType[type].value + " " + loc

    zone = Zone.objects.filter(name=request.user.profile.zone).first()
    if zone is None:
        return HttpResponse("Impossible de trouver la zone gérée pas l'utilisateur", status=400)

    element = Element(name=name, type=type, status=state, location=loc, zone=zone)  # Creation

    log_element(element, request)
    return HttpResponse(element.id, status=200)


def add_report_element(request):
    values = json.loads(request.body.decode("utf-8"))

    for index, elem in enumerate(values["selectedOutlets"]):
        outlet = Element.objects.filter(id=elem).first()
        if outlet is None:
            return HttpResponse("La sortie d'eau concernée par ce rapport n'a pas été trouvée", status=400)

        if not has_access(outlet, request):
            return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

        active = values["isActive"]
        if active:
            hour_activity = values["inputHours"]
            day_activity = values["inputDays"]

            if not is_int(hour_activity) or not is_int(day_activity):
                return HttpResponse("Impossible, certains champs devraient être des entiers", status=400)

            data = values["details"][index]["perCubic"] != "none"
            if data:
                meters_distr = values["details"][index]["cubic"]
                value_meter = values["details"][index]["perCubic"]
                recette = values["details"][index]["bill"]

                if not is_float(meters_distr) or not is_float(value_meter) or not is_float(recette):
                    return HttpResponse("Impossible, certains champs devraient être des entiers", status=400)

                report_line = Report(water_outlet=outlet, was_active=active, has_data=data,
                                     hours_active=hour_activity, days_active=day_activity,
                                     quantity_distributed=meters_distr, price=value_meter, recette=recette)

                if outlet.type == ElementType.INDIVIDUAL.name:  # Create an invoice for individual outlets
                    consumer = Consumer.objects.filter(water_outlet=outlet).first()
                    if consumer and data:
                        amount = int(meters_distr) * int(value_meter)
                        creation = date.today()
                        expiration = creation + relativedelta(months=1)
                        invoice = Invoice(consumer=consumer, water_outlet=outlet, creation=creation,
                                          expiration=expiration, amount=amount)
                        invoice.save()
            else:
                report_line = Report(water_outlet=outlet, was_active=active, has_data=data,
                                     hours_active=hour_activity, days_active=day_activity)
        else:
            report_line = Report(water_outlet=outlet, was_active=active)

        log_element(report_line, request)

    return HttpResponse(status=200)


def add_zone_element(request):
    if request.user.profile.zone is None:
        return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

    name = request.POST.get("name", None)
    fountain_price = request.POST.get("fountain-price", 0)
    fountain_duration = request.POST.get("fountain-duration", 1)
    kiosk_price = request.POST.get("kiosk-price", 0)
    kiosk_duration = request.POST.get("kiosk-duration", 1)

    if not is_int(fountain_price) or not is_int(fountain_duration) \
            or not is_int(kiosk_price) or not is_int(kiosk_duration):
        return HttpResponse("Impossible, certains champs devraient être des entiers", status=400)

    if Zone.objects.filter(name=name).first() is not None:
        return HttpResponse("Une zone avec ce nom existe déjà dans l'application, "
                            "veuillez en choisir un autre", status=400)

    superzone = Zone.objects.filter(name=request.user.profile.zone).first()
    if superzone is None:
        return HttpResponse("Impossible de trouver la zone gérée pas l'utilisateur", status=400)

    zone = Zone(name=name, superzone=superzone, subzones=[name],
                fountain_price=fountain_price, fountain_duration=fountain_duration,
                kiosk_price=kiosk_price, kiosk_duration=kiosk_duration)

    while superzone is not None:
        superzone.subzones.append(name)
        superzone.save()
        superzone = superzone.superzone

    log_element(zone, request)
    return HttpResponse(zone.id, status=200)


def add_collaborator_element(request):
    if request.user.profile.zone is None:
        return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

    first_name = request.POST.get("firstname", None)
    last_name = request.POST.get("lastname", None)
    username = request.POST.get("id", None)
    password = User.objects.make_random_password()  # New random password
    email = request.POST.get("email", None)
    type = request.POST.get("type", None)
    phone = request.POST.get("phone", None)

    if User.objects.filter(username=username).first() is not None:
        return HttpResponse("Cet utilisateur existe déjà ! Vérifier que son identifiant est bien unique", status=400)

    user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=first_name, last_name=last_name)
    user.profile.phone_number = phone

    if type == "fountain-manager":
        outlet_ids = request.POST.get("outlets", None).split(',')
        if len(outlet_ids) < 1:
            user.delete()
            return HttpResponse("Vous n'avez pas choisi de fontaine a attribuer !", status=400)

        outlets = Element.objects.filter(id__in=outlet_ids) if len(outlet_ids) > 1 else \
            Element.objects.filter(id=outlet_ids[0])

        if len(outlets) < 1:
            user.delete()
            return HttpResponse("Impossible d'attribuer cette fontaine au gestionnaire", status=400)

        for outlet in outlets:
            if not has_access(outlet, request):
                return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)
            outlet.manager_names = outlet.get_managers()
            outlet.save()
            user.profile.outlets.append(outlet.id)

        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        my_group.user_set.add(user)
    elif type == "zone-manager":
        zone_id = request.POST.get("zone", None)
        zone = Zone.objects.filter(id=zone_id).first()
        if zone is None:
            user.delete()
            return HttpResponse("Impossible d'attribuer cette zone au gestionnaire", status=400)

        user.profile.zone = zone

        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(user)
    else:
        user.delete()
        return HttpResponse("Impossible d'ajouter l'utilisateur", status=400)

    send_mail('Bienvenue sur haitiwater !',
              'Bienvenue sur haitiwater. Voici votre mot de passe autogénéré : ' + password + '\n' +
              'Veuillez vous connecter pour le modifier.\n' +
              'Pour rappel, votre identifiant est : ' + username,
              '', [email], fail_silently=False)

    log_element(user.profile, request)
    return HttpResponse(user.id, status=200)


def add_ticket_element(request):
    outlet_id = request.POST.get("id_outlet", None)
    type = request.POST.get("type", None).upper()
    comment = request.POST.get("comment", None)
    urgency = request.POST.get('urgency', None).upper()
    image = request.FILES.get("picture", None)

    outlet = Element.objects.filter(id=outlet_id).first()
    if outlet is None:
        return HttpResponse("Impossible de trouver la sortie d'eau correspondante au ticket", status=400)

    if not has_access(outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

    if image:
        import uuid
        extension = image.name.split(".")
        filename = str(uuid.uuid4())
        image.name = filename + "." + extension[1]

    ticket = Ticket(water_outlet=outlet, type=type, comment=comment, urgency=urgency, image=image)

    log_element(ticket, request)
    return HttpResponse(ticket.id, status=200)


def add_payment_element(request):
    id_consumer = request.POST.get("id_consumer", None)
    amount = request.POST.get("amount", None)

    if not is_float(amount):
        return HttpResponse("Impossible, certains champs devraient être des entiers", status=400)

    consumer = Consumer.objects.filter(id=id_consumer).first()
    if not consumer:
        return HttpResponse("Impossible de trouver l'utilisateur", status=400)
    elif not has_access(consumer.water_outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur ce consommateur", status=403)

    outlet = consumer.water_outlet
    payment = Payment(consumer=consumer, water_outlet=outlet, amount=amount)

    log_element(payment, request)
    return HttpResponse(payment.id, status=200)


def add_location_element(request, elem):
    body = request.body.decode('utf-8')
    json_value = json.loads(body)

    poly = GEOSGeometry(str(json_value["geometry"]))
    lon, lat = 0, 0
    if len(poly.coord_seq) == 1:
        lon, lat = poly[0], poly[1]

    loc = Location(elem=elem, lat=lat, lon=lon, poly=poly, json_representation=body)

    log_element(loc, request)
    return HttpResponse(loc.id, status=200)
