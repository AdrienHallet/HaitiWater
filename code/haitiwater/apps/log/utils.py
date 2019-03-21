import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import ManyToOneRel, OneToOneRel
from django.http import HttpResponse

from .models import Log, Transaction


def log_add(table, column, value, transaction):
    if transaction.is_visible():
        transaction.save()
        new_val = Log(action="ADD", table_name=table, column_name=column,
                  new_value=value, transaction=transaction)
        new_val.save()
    else: #If no one has the hierarchical status to see the transactions + log, don't save them in DB
        transaction.save()
        transaction.delete()


def log_delete(table, column, value, transaction):
    if transaction.is_visible():
        transaction.save()
        new_val = Log(action="DELETE", table_name=table, column_name=column,
                  old_value=value, transaction=transaction)
        new_val.save()
    else:
        transaction.save()
        transaction.delete()


def log_edit(table, column, old_val, new_val, transaction):
    if transaction.is_visible():
        transaction.save()
        new_val = Log(action="EDIT", table_name=table, column_name=column,
                  old_value=old_val, new_value=new_val, transaction=transaction)
        new_val.save()
    else:
        transaction.save()
        transaction.delete()


def roll_back(transaction):
    logs = Log.objects.filter(transaction=transaction)
    if logs[0].action == "EDIT": #Edit case
        elements = get_elem_logged(logs)
        tables = get_concerned_tables(logs)
        for number, table in enumerate(tables):
            roll_back_item(
                elements[number],
                {log.column_name: log.old_value
                       for log in logs
                       if log.table_name == table and log.column_name != "ID"}
            )
        log_finished(transaction, "CANCEL")
    elif logs[0].action == "ADD": #Add case
        elements = get_elem_logged(logs)
        for elem in elements:
            elem.delete()
        log_finished(transaction, "CANCEL")
    elif logs[0].action == "DELETE": #Delete case
        re_add_item(logs)
        log_finished(transaction, "CANCEL")


def get_concerned_tables(logs):
    tables = []
    for log in logs:
        if log.column_name == "ID":
            tables.append(log.table_name)
    return tables


def log_finished(transaction, action):
    #Archive
    transaction.archived = True
    now = datetime.datetime.now().date()
    transaction.date_archived = now
    transaction.action = action
    transaction.save()
    #Check to flush if needed #TODO : Maybe do a cron job on this
    delta = datetime.timedelta(weeks=3) #Delta of three weeks
    for old_transaction in Transaction.objects.filter(archived=True):
        if old_transaction.date_archived + delta <= now \
                and old_transaction != transaction: #If we need to flush this
            for log in Log.objects.filter(transaction=old_transaction):
                log.delete()
            old_transaction.delete()


def roll_back_item(item, values):
    if "Role" in values or "_zone" in values or "_outlets" in values:#Change of user, handle separately
        if values["Role"] == "Gestionnaire de fontaine":
            from django.contrib.auth.models import Group
            my_group = Group.objects.get(name='Gestionnaire de fontaine')
            other_group = Group.objects.get(name='Gestionnaire de zone')
            other_group.user_set.remove(item)
            my_group.user_set.add(item)
        if values["Role"] == "Gestionnaire de zone":
            from django.contrib.auth.models import Group
            my_group = Group.objects.get(name='Gestionnaire de zone')
            other_group = Group.objects.get(name='Gestionnaire de fontaine')
            other_group.user_set.remove(item)
            my_group.user_set.add(item)
        if values["_zone"] and values["_zone"] != "Rien":
            from ..water_network.models import Zone
            item.profile.zone = Zone.objects.filter(id=values["_zone"]).first()
            item.profile.outlets = []
        if values["_outlets"] and values["_outlets"] != "Rien":
            from ..water_network.models import Element
            import ast
            water_out = ast.literal_eval(values["_outlets"])
            if len(water_out) < 1:
                return
            elif len(water_out) > 1:
                res = Element.objects.filter(id__in=water_out)
            else:
                res = Element.objects.filter(id=water_out[0])
            if len(res) > 0:
                item.profile.outlets = []
                for outlet in res:
                    item.profile.outlets.append(outlet.id)
                item.profile.zone = None
        item.save()
        return
    all_attributes = item._meta.get_fields()
    for verbose_field, value in values.items():
        for field in all_attributes:
            if type(field) != ManyToOneRel and type(field) != OneToOneRel and\
                    verbose_field == field.verbose_name \
                    and verbose_field != "ID":
                if field.name == "type":
                    item.type = values["_type"]
                elif field.name == "status":
                    item.status = values["_status"]
                elif field.name == "urgency":
                    item.status = values["_urgency"]
                elif field.name == "zone":
                    from ..water_network.models import Zone
                    zone = Zone.objects.get(values["_zone"])
                    item.zone = zone
                elif field.name == "gender":
                    item.gender = values["_gender"]
                else:
                    item.__setattr__(field.name, value)
    item.save()


def re_add_item(logs):
    tables = get_concerned_tables(logs)
    for table in tables:
        restore_item(
            {log.column_name: log.old_value
                for log in logs
                if log.table_name == table and log.column_name != "ID"},
                table)


def restore_item(dict, table):
    if table == "consumer":
        restore_consumer(dict)
    elif table == "ticket":
        restore_ticket(dict)
    elif table == "element":
        restore_water_element(dict)
    elif table == "zone":
        restore_zone(dict)
    elif table == "report":
        pass
    elif table == "profile":
        restore_user(dict)
    elif table == "payment":
        restore_payment(dict)
    elif table == "location":
        restore_location(dict)


def restore_consumer(dict):
    from ..water_network.models import Element
    from ..consumers.models import Consumer
    outlet = Element.objects.filter(id=dict["_water_outlet"])
    if len(outlet) != 1:
        return HttpResponse("Impossible de restaurer cet élément", status=500)
    outlet = outlet[0]
    restored = Consumer(last_name=dict["Nom"], first_name=dict["Prénom"],
                        gender=dict["_gender"], location=dict["Adresse"],
                        phone_number=dict["Numéro de téléphone"] if dict["Numéro de téléphone"] != "Non spécifié" else "0",
                        email="", household_size=dict["Taille du ménage"], creation_date=dict["Date de création"],
                        water_outlet=outlet)
    restored.save()


def restore_ticket(dict):
    from ..water_network.models import Element
    from ..report.models import Ticket
    outlet = Element.objects.filter(id=dict["Sortie d'eau concernée"])
    if len(outlet) != 1:
        return HttpResponse("Impossible de restaurer cet élément", status=500)
    outlet = outlet[0]
    restored = Ticket(water_outlet=outlet, type=dict["_type"],
                      comment=dict["Commentaire"], urgency=dict["_urgency"],
                      status=dict["_status"], image=None)
    restored.save()


def restore_water_element(dict):
    from ..water_network.models import Element, Zone
    zone = Zone.objects.filter(id=dict["_zone"])
    if len(zone) != 1:
        return HttpResponse("Impossible de restaurer cet élément", status=500)
    zone = zone[0]
    restored = Element(name=dict["Nom"], type=dict["_type"],
                       status=dict["_status"], location=dict["Localisation"],
                       zone=zone)
    restored.save()


def restore_zone(dict):
    from ..water_network.models import Zone
    id_zone = dict["Zone mère"].split()[0]
    super_zone = Zone.objects.filter(id=id_zone)
    if len(super_zone) != 1:
        return HttpResponse("Impossible de restaurer cet élément", status=500)
    super_zone = super_zone[0]
    restored = Zone(name=dict["Nom"], superzone=super_zone, subzones=[],
                    fountain_duration=dict["Durée de la souspricption des fontaines"],
                    fountain_price=dict["Prix des fontaines"],
                    kiosk_duration=dict["Durée de la souspricption des kiosques"],
                    kiosk_price=dict["Prix des kiosques"])
    up = True
    while up:
        super_zone.subzones.append(dict["Nom"])
        super_zone.save()
        super_zone = super_zone.superzone
        if super_zone is None:
            up = False
    restored.save()


def restore_user(dict):
    from ..water_network.models import Element, Zone
    from django.contrib.auth.models import User, Group
    password = User.objects.make_random_password()  # New random password
    user = User.objects.create_user(username=dict["Identifiant"],
                                    email=dict["Email"],
                                    password=password,
                                    first_name=dict["Prénom"],
                                    last_name=dict["Nom de famille"])

    if dict["Role"] == "Gestionnaire de fontaine":
        import ast
        water_out = ast.literal_eval(dict["_outlets"])
        if len(water_out) < 1:
            return HttpResponse("Vous n'avez pas choisi de fontaine a attribuer !", status=500)
        elif len(water_out) > 1:
            res = Element.objects.filter(id__in=water_out)
        else:
            res = Element.objects.filter(id=water_out[0])
        if len(res) > 0:
            user.profile.outlets = []
            for outlet in res:
                user.profile.outlets.append(outlet.id)
        else:
            return HttpResponse("Impossible d'attribuer cette fontaine au gestionnaire", status=404)
        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        other_group = Group.objects.get(name='Gestionnaire de zone')
        other_group.user_set.remove(user)
        my_group.user_set.add(user)
        user.save()
    elif dict["Role"] == "Gestionnaire de zone":
        zone = dict["_zone"]
        res = Zone.objects.filter(id=zone)
        if len(res) == 1:
            user.profile.zone = res[0]
            user.save()
        else:
            user.delete()
            return HttpResponse("Impossible d'attribuer cette zone au gestionnaire", status=404)
        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(user)
        other_group = Group.objects.get(name='Gestionnaire de fontaine')
        other_group.user_set.remove(user)
        user.save()
    else:
        user.delete()
        return HttpResponse("Impossible d'ajouter l'utilisateur", status=500)
    send_mail(
        'Changement de mot de passe.',
        'Votre compte haitiwater a été modifié, vous devez donc en changer le mot de passe.' +
        '\nVoici votre nouveau mot de passe autogénéré : ' + password +
        '\nVeuillez vous connecter pour le modifier.\nPour rappel, ' +
        'votre identifiant est : ' + dict["Identifiant"],
        '',
        [dict["Email"]],
        fail_silently=False,
    )


def restore_payment(dict):
    from ..financial.models import Payment
    from ..water_network.models import Element
    from ..consumers.models import Consumer
    cons = Consumer.objects.get(id=dict["Identifiant consommateur"])
    water = Element.objects.get(id=dict["Identifiant point d'eau"])
    payment = Payment(consumer=cons, water_outlet=water,
                      amount=dict["Montant"], date=dict["Date de la facture"])
    payment.save()


def restore_location(dict):
    from ..water_network.models import Location, Element
    elem = Element.objects.get(id=dict["Identifiant de l'élément"])
    location = Location(poly=dict["_poly"], json_representation=dict["_json"],
                        elem=elem, lat=dict["Latitude"], lon=dict["Longitude"])
    location.save()


def get_elem_logged(logs):
    from ..water_network.models import Element, Zone, Location
    from ..report.models import Report, Ticket
    from ..consumers.models import Consumer
    from ..financial.models import Payment
    tables = get_concerned_tables(logs)
    ids = []
    for elem in logs:
        if elem.column_name =="ID":
            ids.append(elem.new_value)
    elems = []
    for number, table in enumerate(tables):
        elem = None
        if table == "consumer":
            elem = Consumer.objects.get(id=ids[number])
        elif table == "ticket":
            elem = Ticket.objects.get(id=ids[number])
        elif table == "element":
            elem = Element.objects.get(id=ids[number])
        elif table == "zone":
            elem = Zone.objects.get(id=ids[number])
        elif table == "report":
            elem = Report.objects.get(id=ids[number])
        elif table == "profile":
            elem = User.objects.get(id=ids[number])
        elif table == "payment":
            elem = Payment.objects.get(id=ids[number])
        elif table == "location":
            elem = Location.objects.get(id=ids[number])
        if elem is not None:
            elems.append(elem)
    return elems
