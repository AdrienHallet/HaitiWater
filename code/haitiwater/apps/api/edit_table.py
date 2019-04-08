import json
from datetime import date

from django.contrib.auth.models import User, Group
from django.http import HttpResponse

from ..consumers.models import Consumer
from ..financial.models import Invoice, Payment
from ..log.models import Transaction, Log
from ..report.models import Ticket, Report
from ..utils.get_data import has_access
from ..water_network.models import Element, ElementType, Zone

success_200 = HttpResponse(status=200)


def log_element(element, old, request):
    transaction = Transaction(user=request.user)
    transaction.save()
    element.save()
    element.log_edit(old, transaction)
    clean_up(element)


def clean_up(element):
    logs = Log.objects.filter(action="EDIT", column_name="ID", table_name=element._meta.model_name,
                              new_value=element.id, transaction__archived=False)
    if len(logs) != 0 and element._meta.model_name != "profile":  # If we found a logs modifying this element
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


def edit_water_element(request):
    elem_id = request.POST.get("id", None)
    elem = Element.objects.filter(id=elem_id).first()
    if elem is None:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=400)

    if not has_access(elem, request):
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

    old = elem.infos()
    elem.type = request.POST.get("type", None).upper()
    elem.location = request.POST.get("localization", None)
    elem.status = request.POST.get("state", None).upper()
    elem.name = elem.get_type() + " " + elem.location

    log_element(elem, old, request)
    return success_200


def edit_consumer(request):
    consumer_id = request.POST.get("id", None)
    consumer = Consumer.objects.filter(id=consumer_id).first()
    if consumer is None:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=400)

    if not has_access(consumer.water_outlet, request):  # TODO check if good heuristic
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

    old = consumer.infos()
    consumer.first_name = request.POST.get("firstname", None)
    consumer.last_name = request.POST.get("lastname", None)
    consumer.gender = request.POST.get("gender", None)
    consumer.location = request.POST.get("address", None)
    consumer.household_size = request.POST.get("subconsumer", None)
    consumer.phone_number = request.POST.get("phone", None)
    outlet_id = request.POST.get("mainOutlet", None)

    outlet = Element.objects.filter(id=outlet_id).first()
    if outlet is None:
        return HttpResponse("Impossibe de trouver cet élément du réseau", status=400)

    if not has_access(outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

    old_outlet = consumer.water_outlet
    consumer.water_outlet = outlet

    log_element(consumer, old, request)

    if old_outlet != outlet and not outlet.type == ElementType.INDIVIDUAL.name:
        old_invoice = Invoice.objects.filter(water_outlet=old_outlet, expiration__gt=date.today()).first()
        if old_invoice:
            old_invoice.expiration = date.today()
            price, duration = outlet.get_price_and_duration()
            creation = date.today()
            expiration = creation + relativedelta(months=duration)
            invoice = Invoice(consumer=consumer, water_outlet=outlet, amount=price,
                              creation=creation, expiration=expiration)
            invoice.save()

    return success_200


def edit_zone(request):
    if request.user.profile.zone is None:
        return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

    zone_id = request.POST.get("id", None)
    zone = Zone.objects.filter(id=zone_id).first()
    if zone is None:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=400)

    if zone.name not in request.user.profile.zone.subzones:
        return HttpResponse("Vous n'avez pas les droits sur cette zone", status=403)

    old = zone.infos()
    old_name = zone.name
    zone.name = request.POST.get("name", None)
    zone.fountain_price = request.POST.get("fountain-price", 0)
    zone.fountain_duration = request.POST.get("fountain-duration", 1)
    zone.kiosk_price = request.POST.get("kiosk-price", 0)
    zone.kiosk_duration = request.POST.get("kiosk-duration", 1)
    zone.indiv_base_price = request.POST.get("indiv-price", 0)

    zone.subzones.remove(old_name)
    zone.subzones.append(zone.name)
    for superzone in Zone.objects.filter(subzones__contains=[old_name]):
        superzone.subzones.remove(old_name)
        superzone.subzones.append(zone.name)
        superzone.save()

    log_element(zone, old, request)
    return success_200


def edit_ticket(request):
    ticket_id = request.POST.get("id", None)
    ticket = Ticket.objects.filter(id=ticket_id).first()
    if ticket is None:
        return HttpResponse("Impossible de trouver l'élément que vous voulez éditer", status=400)

    old = ticket.infos()
    id_outlet = request.POST.get("id_outlet", None)
    outlet = Element.objects.filter(id=id_outlet).first()
    if outlet is None:
        return HttpResponse("Impossible de trouver l'élément du réseau associé", status=400)
    if not has_access(outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

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
    return success_200


def edit_manager(request):
    if request.user.profile.zone is None:
        return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

    user_id = request.POST.get("id", None)
    user = User.objects.filter(username=user_id).first()
    if user is None:
        return HttpResponse("Impossible de trouver cet utilisateur", status=400)

    old = user.profile.infos()
    phone = request.POST.get("phone", None)
    user.profile.phone_number = phone
    type = request.POST.get("type", None)

    if type == "fountain-manager":
        outlets = request.POST.get("outlets", None)
        outlets = outlets.split(',')

        if len(outlets) < 1:
            return HttpResponse("Vous n'avez pas choisi de fontaine a attribuer !", status=400)
        if len(outlets) > 1:
            res = Element.objects.filter(id__in=outlets)
        else:
            res = Element.objects.filter(id=outlets[0])

        if len(outlets) == 0:
            return HttpResponse("Impossible d'attribuer cette fontaine au gestionnaire", status=400)

        old_outlets = user.profile.outlets
        user.profile.outlets = []
        for outlet in res:
            if not has_access(outlet, request):
                return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)
            outlet.manager_names = outlet.get_managers()
            outlet.save()
            user.profile.outlets.append(outlet.id)

        if len(old_outlets) > 0:
            if len(old_outlets) > 1:
                res2 = Element.objects.filter(id__in=old_outlets)
            else:
                res2 = Element.objects.filter(id=old_outlets[0])
            for outlet in res2:
                outlet.manager_names = outlet.get_managers()
                outlet.save()

        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        my_group.user_set.add(user)
        if user.profile.zone:  # If user had a zone, switch it
            g = Group.objects.get(name='Gestionnaire de zone')
            g.user_set.remove(user)
            user.profile.zone = None

        log_element(user.profile, old, request)

    elif type == "zone-manager":
        zone_id = request.POST.get("zone", None)
        zone = Zone.objects.filter(id=zone_id).first()
        if zone is None:
            return HttpResponse("Impossible d'assigner cette zone", status=400)
        if zone.name not in request.user.profile.zone.subzones:
            return HttpResponse("Vous n'avez pas les droits sur cette zone", status=403)

        user.profile.zone = zone

        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(user)
        if len(user.profile.outlets) > 0:  # If user had outlets
            g = Group.objects.get(name='Gestionnaire de fontaine')
            g.user_set.remove(user)
            user.profile.outlets = []

        log_element(user.profile, old, request)

    return success_200


def edit_payment(request):
    payment_id = request.POST.get("id", None)
    payment = Payment.objects.filter(id=payment_id).first()
    if payment is None:
        return HttpResponse("Impossible de trouver ce paiement", status=400)

    old = payment.infos()
    id_consumer = request.POST.get("id_consumer", None)
    consumer = Consumer.objects.filter(id=id_consumer).first()
    if consumer is None:
        return HttpResponse("Impossible de trouver l'utilisateur", status=400)
    elif not has_access(consumer.water_outlet, request):
        return HttpResponse("Vous n'avez pas les droits sur ce consommateur", status=403)

    payment.consumer = consumer
    payment.water_outlet = consumer.water_outlet
    payment.amount = request.POST.get("amount", None)

    log_element(payment, old, request)
    return success_200


def edit_report(request):
    values = json.loads(request.body.decode("utf-8"))
    year = values["date"].split("-")[0]
    month = values["date"].split("-")[1]
    for elem in values["details"]:
        report = Report.objects.filter(water_outlet_id=elem["id"], timestamp__month=month, timestamp__year=year).first()
        if report is None:
            return HttpResponse("Impossible de trouver ce rapport", status=400)

        old = report.infos()
        report.has_data = elem["has_data"]
        if elem["has_data"]:
            # Days active
            if True:  # TODO was active
                report.quantity_distributed = elem["volume"]
                report.price = elem["price"]
                report.recette = elem["revenue"]
                # TODO change invoice ?
        log_element(report, old, request)
    return success_200
