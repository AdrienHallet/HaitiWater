import re

from django.core.cache import cache

from ..api.add_table import *
from ..api.edit_table import *
from ..log.utils import *
from ..utils.get_data import is_user_zone, is_user_fountain, get_outlets
from ..water_network.models import ElementType, ElementStatus

success_200 = HttpResponse(status=200)


def graph(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    json_object = {"jsonarray": []}

    export_format = request.GET.get('type', None)
    if export_format == "consumer_gender_pie":
        json_object["jsonarray"].append({'label': "Femmes", 'data': 0})
        json_object["jsonarray"].append({'label': "Hommes", 'data': 0})
        json_object["jsonarray"].append({'label': "Autres", 'data': 0})

        consumers = None
        if is_user_fountain(request):
            consumers = Consumer.objects.filter(water_outlet__id__in=request.user.profile.outlets)
        elif is_user_zone(request):
            consumers = Consumer.objects.filter(water_outlet__zone__name__in=request.user.profile.zone.subzones)

        for consumer in consumers:
            if consumer.gender == "F" or consumer.gender == "Femme":
                json_object['jsonarray'][0]['data'] += 1  # One more women
            elif consumer.gender == "M" or consumer.gender == "Homme":
                json_object['jsonarray'][1]['data'] += 1  # One more man
            else:
                json_object['jsonarray'][2]['data'] += 1  # One more other

    if export_format == "average_monthly_volume_per_zone":
        elements = []
        data = []

        if is_user_fountain(request):
            for outlet in Element.objects.filter(id__in=request.user.profile.outlets):
                elements.append(outlet.name)

                total = 0
                no_data = True
                for report in Report.objects.filter(water_outlet=outlet):
                    if report.was_active and report.has_data:
                        no_data = False
                        total += report.quantity_distributed

                data.append(total if not no_data else None)

        elif is_user_zone(request):
            for zone in Zone.objects.filter(name__in=request.user.profile.zone.subzones):
                elements.append(zone.name)

                total = 0
                no_data = True
                for report in Report.objects.filter(water_outlet__zone__name__in=zone.subzones):
                    if report.was_active and report.has_data:
                        no_data = False
                        total += report.quantity_distributed

                data.append(total if not no_data else None)

        json_object["jsonarray"].append({"label": elements, "data": data})

    return HttpResponse(json.dumps(json_object))


def gis_infos(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    if request.method == "GET":
        locations = None
        if is_user_fountain(request):
            locations = Location.objects.filter(elem_id__in=request.user.profile.outlets)
        elif is_user_zone(request):
            locations = Location.objects.filter(elem__zone__name__in=request.user.profile.zone.subzones)

        markers = request.GET.get("marker", None)
        if markers == "fountain":
            locations = locations.filter(elem__type=ElementType.FOUNTAIN.name)
        elif markers == "kiosk":
            locations = locations.filter(elem__type=ElementType.KIOSK.name)
        elif markers == "individual":
            locations = locations.filter(elem__type=ElementType.INDIVIDUAL.name)
        elif markers == "not in service":
            locations = locations.exclude(elem__status=ElementStatus.OK.name)

        results = {}
        for location in locations:
            results[location.elem.id] = [location.elem.name, location.json_representation]
        return HttpResponse(json.dumps(results))

    elif request.method == "POST":
        elem_id = request.GET.get("id", None)
        elem = Element.objects.filter(id=elem_id).first()
        if elem is None:
            return HttpResponse("Impossible de trouver l'élément demandé", status=400)
        elif not has_access(elem, request):
            return HttpResponse("Vous n'avez pas les droits sur cet élément de réseau", status=403)

        action = request.GET.get("action", None)
        if action == "add":
            return add_location_element(request, elem)
        elif action == "remove":
            loc = Location.objects.filter(elem_id=elem_id).first()
            if loc is None:
                return HttpResponse("Impossible de trouver l'élément demandé", status=400)

            log_element(loc, request)
            loc.delete()
            return success_200
        else:
            return HttpResponse("Impossible de traiter cette requête", status=400)


# https://datatables.net/manual/server-side
def table(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    params = parse(request)
    table_name = params["table_name"]
    last_draw = request.GET.get('draw', "0")  # 1 ?
    json_object = {
        "draw": str(int(last_draw) + 1),
        "editable": True,  # custom field, true to display edit/delete buttons
        "data": []
    }

    cache_key = table_name + request.user.username
    cache_result = cache.get(cache_key) if table_name != "payment" else None

    if cache_result:
        result = json.loads(cache_result)
        cache.touch(cache_key, 60)
    elif table_name == "water_element":
        if is_user_fountain(request):
            json_object["editable"] = False
        result = get_water_elements(request)
    elif table_name == "consumer":
        result = get_consumer_elements(request)
    elif table_name == "zone":
        if is_user_fountain(request):
            return HttpResponse("Vous ne pouvez pas accéder à ces informations", status=403)
        result = get_zone_elements(request)
    elif table_name == "manager":
        if is_user_fountain(request):
            return HttpResponse("Vous ne pouvez pas accéder à ces informations", status=403)
        result = get_manager_elements(request)
    elif table_name == "report":
        if is_user_zone(request):
            return HttpResponse("Vous ne pouvez pas accéder à ces informations", status=403)
        result = get_last_reports(request)
    elif table_name == "ticket":
        result = get_ticket_elements(request)
    elif table_name == "logs":
        result = get_logs_elements(request, archived=False)
    elif table_name == "logs_history":
        result = get_logs_elements(request, archived=True)
    elif table_name == "payment":
        if is_user_fountain(request):
            json_object["editable"] = False
        result = get_payment_elements(request)
        if result is None:
            return success_200
    else:
        return HttpResponse("Impossible de charger la table demandée (" + table_name + ").", status=404)

    if result is None:
        return HttpResponse("Problème à la récupération des données", status=400)

    cache.set(cache_key, json.dumps(result), 60)
    json_object["recordsTotal"] = len(result)

    filtered = filter_search(params, result)

    if table_name == "logs" or table_name == "logs_history" or table_name == "report":
        if len(filtered) > 1:
            keys = list(filtered[0].keys())
            final = sorted(filtered, key=lambda x: x[keys[params["column_ordered"]]],
                           reverse=params["type_order"] != "asc")
        else:
            final = filtered
    else:
        final = sorted(filtered, key=lambda x: x[params["column_ordered"]],
                       reverse=params["type_order"] != "asc")

    if params["length_max"] == -1:
        json_object["data"] = final
    else:
        start = params["start"]
        stop = start + params["length_max"]
        json_object["data"] = final[start:stop]

    json_object["recordsFiltered"] = len(final)
    return HttpResponse(json.dumps(json_object), status=200)


def add_element(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    element = request.POST.get("table", "")

    cache_key = element + request.user.username
    cache.delete(cache_key)

    if element == "water_element":
        return add_network_element(request)
    elif element == "consumer":
        return add_consumer_element(request)
    elif element == "zone":
        return add_zone_element(request)
    elif element == "manager":
        cache_key = "water_element" + request.user.username
        cache.delete(cache_key)
        return add_collaborator_element(request)
    elif element == "ticket":
        return add_ticket_element(request)
    elif element == "payment":
        return add_payment_element(request)
    else:
        return HttpResponse("Impossible d'ajouter l'élément " + element, status=400)


def remove_element(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    element = request.POST.get("table", "")

    cache_key = element + request.user.username
    cache.delete(cache_key)

    if element == "water_element":
        element_id = request.POST.get("id", None)

        consumers = Consumer.objects.filter(water_outlet=element_id)
        if len(consumers) > 0:
            return HttpResponse("Vous ne pouvez pas supprimer cet élément, il est encore attribué à " +
                                "des consommateurs", status=400)

        elem_delete = Element.objects.filter(id=element_id).first()
        if elem_delete is None:
            return HttpResponse("Impossible de supprimer cet élément, il n'existe pas", status=400)
        elif not has_access(elem_delete, request):
            return HttpResponse("Impossible de supprimer cet élément, vous n'avez pas les droits", status=403)

        transaction = Transaction(user=request.user)
        if not is_same(elem_delete, request.user):
            transaction.save()
            elem_delete.log_delete(transaction)

        elem_delete.delete()

        tickets = Ticket.objects.filter(water_outlet=element_id)
        for t in tickets:
            if not is_same(t, request.user):
                t.log_delete(transaction)
            t.delete()

        for user in User.objects.filter(profile__outlets__contains=[str(element_id)]):
            old = user.profile.infos()
            user.profile.outlets.remove(str(element_id))
            user.save()
            user.profile.log_edit(old, transaction)

        return success_200

    elif element == "consumer":
        consumer_id = request.POST.get("id", None)
        to_delete = Consumer.objects.filter(id=consumer_id).first()
        if to_delete is None:
            return HttpResponse("Impossible de supprimer ce consommateur, il n'existe pas", status=400)
        elif not has_access(to_delete.water_outlet, request):
            return HttpResponse("Impossible de supprimer ce consommateur, vous n'avez pas les droits", status=403)

        log_element(to_delete, request)
        to_delete.delete()

        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)

    elif element == "manager":
        if request.user.profile.zone is None:
            return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

        manager_id = request.POST.get("id", None)
        to_delete = User.objects.filter(username=manager_id).first()
        if to_delete is None:
            return HttpResponse("Impossible de supprimer cet utilisateur, il n'existe pas", status=400)
        if to_delete.id == 1 or to_delete.id == 2:  # IDs 1 and 2 are superuser and admin, should not be removed
            return HttpResponse("Impossible de supprimer cet utilisateur, il est nécéssaire au fonctionnement de"
                                " l'application. Vous pouvez cependant le modifier", status=400)
        elif to_delete.profile.zone and to_delete.profile.zone.name not in request.user.profile.zone.subzones:
            return HttpResponse("Impossible de supprimer cet utilisateur, vous n'avez pas les droits", status=403)
        else:
            for outlet_id in to_delete.profile.outlets:
                outlet = Element.objects.filter(id=outlet_id).first()
                if outlet is None:
                    return HttpResponse("Impossible de supprimer cet utilisateur, " +
                                        "il est lié à une fontaine dont la zone n'existe pas", status=400)
                elif outlet.zone.name not in request.user.profile.zone.subzones:
                    return HttpResponse("Impossible de supprimer cet utilisateur, vous n'avez pas les droits",
                                        status=403)

        log_element(to_delete.profile, request)
        to_delete.delete()

        cache_key = "water_element" + request.user.username
        cache.delete(cache_key)

        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)

    elif element == "ticket":
        ticket_id = request.POST.get("id", None)
        to_delete = Ticket.objects.filter(id=ticket_id).first()
        if to_delete is None:
            return HttpResponse("Impossible de supprimer ce ticket, il n'existe pas", status=400)
        elif not has_access(to_delete.water_outlet, request):
            return HttpResponse("Impossible de supprimer ce ticket, vous n'avez pas les droits", status=403)

        log_element(to_delete, request)
        to_delete.delete()

        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)

    elif element == "payment":
        payment_id = request.POST.get("id", None)
        to_delete = Payment.objects.filter(id=payment_id).first()
        if to_delete is None:
            return HttpResponse("Impossible de supprimer ce ticket, il n'existe pas", status=400)
        elif not has_access(to_delete.water_outlet, request):
            return HttpResponse("Impossible de supprimer ce ticket, vous n'avez pas les droits", status=403)

        log_element(to_delete, request)
        to_delete.delete()

        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)

    elif element == "zone":
        if request.user.profile.zone is None:
            return HttpResponse("Vous n'êtes pas connecté en tant que gestionnaire de zone", status=403)

        zone_id = request.POST.get("id", None)
        to_delete = Zone.objects.filter(id=zone_id).first()
        if to_delete is None:
            return HttpResponse("Impossible de supprimer cette zone, elle n'existe pas", status=400)
        if to_delete.id == 1:
            return HttpResponse("Impossible de supprimer cette zone, elle est essentielle au fonctionnement de "
                                "l'application. Vous pouvez cependant la modifier.", status=400)
        elif to_delete.name not in request.user.profile.zone.subzones:
            return HttpResponse("Impossible de supprimer cette zone, vous n'avez pas les droits", status=403)

        if len(to_delete.subzones) > 1:
            return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle contient encore" +
                                " d'autres zones", status=400)
        elements = Element.objects.filter(zone=zone_id)
        if len(elements) > 0:
            return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle contient encore" +
                                " des élements du réseau", status=400)
        users = User.objects.filter(profile__zone=to_delete)
        if len(users) > 0:
            return HttpResponse("Vous ne pouvez pas supprimer cette zone, elle est encore attribuée à" +
                                " un gestionnaire de zone", status=400)

        transaction = Transaction(user=request.user)
        for zone in Zone.objects.filter(subzones__contains=[to_delete.name]):
            old = zone.infos()
            zone.subzones.remove(str(to_delete.name))
            zone.save()
            zone.log_edit(old, transaction)

        if not is_same(to_delete, request.user):
            to_delete.log_delete(transaction)
        transaction.save()
        to_delete.delete()

        return HttpResponse({"draw": request.POST.get("draw", 0) + 1}, status=200)

    else:
        return HttpResponse("Impossible de trouver l'élement " + element, status=400)


def edit_element(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    element = request.POST.get("table", "")

    cache_key = element + request.user.username
    cache.delete(cache_key)

    if not element:
        element = request.GET.get("table", None)
    if element == "water_element":
        return edit_water_element(request)
    elif element == "consumer":
        return edit_consumer(request)
    elif element == "zone":
        return edit_zone(request)
    elif element == "ticket":
        return edit_ticket(request)
    elif element == "manager":
        cache_key = "water_element" + request.user.username
        cache.delete(cache_key)
        return edit_manager(request)
    elif element == "payment":
        return edit_payment(request)
    elif element == "report":
        return edit_report(request)
    else:
        return HttpResponse("Impossible d'éditer la table " + element + ", elle n'est pas reconnue", status=400)


def details(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    table_name = request.GET.get("table", None)
    if table_name == "payment":
        return get_payment_details(request)
    elif table_name == "water_element":
        return get_details_network(request)
    else:
        return HttpResponse("Impossible d'obtenir des détails pour la table " + table_name +
                            ", elle n'est pas reconnue", status=400)


def outlets(request):
    if not request.user.is_authenticated:
        return HttpResponse("Vous n'êtes pas connecté", status=403)

    result = {"data": get_outlets(request)}
    return HttpResponse(json.dumps(result))


def compute_logs(request):
    id_val = request.GET.get("id", -1)
    action = request.GET.get("action", None)
    if id_val == -1 or action is None:
        return HttpResponse("Impossible de valider/annuler ce changement", status=400)

    cache_key = "logs" + request.user.username
    cache_key2 = "logs_history" + request.user.username

    transaction = Transaction.objects.filter(id=id_val).first()
    if transaction is None:
        return HttpResponse("Impossible d'identifier le changement", status=400)

    if action == "accept":
        log_finished(transaction, "ACCEPT")
        cache.delete(cache_key)
        cache.delete(cache_key2)
        return success_200
    elif action == "revert":
        roll_back(transaction)
        cache.delete(cache_key)
        cache.delete(cache_key2)
        return success_200
    else:
        return HttpResponse("Action non reconnue", status=400)


def log_element(element, request):
    if not is_same(element, request.user):
        transaction = Transaction(user=request.user)
        transaction.save()
        element.log_delete(transaction)


def is_same(element, user):
    log = Log.objects.filter(action="ADD", column_name="ID", table_name=element._meta.model_name,
                             new_value=element.id, transaction__archived=False).first()
    if log is None:
        return False

    transaction = log.transaction
    if transaction.user != user or transaction.archived:
        return False

    all_logs = Log.objects.filter(transaction=transaction)
    for log in all_logs:
        log.delete()

    transaction.delete()
    return True


def parse(request):
    column_regex = re.compile('order\[\d*\]\[column\]')
    dir_regex = re.compile('order\[\d*\]\[dir\]')

    columns = list(filter(column_regex.match, dict(request.GET).keys()))
    dirs = list(filter(dir_regex.match, dict(request.GET).keys()))

    searchable_cols = []
    for i in range(25):
        if request.GET.get('columns[' + str(i) + '][searchable]', False):
            searchable_cols.append(i)

    params = {
        "table_name": request.GET.get('name', None),
        "length_max": int(request.GET.get('length', 10)),
        "start": int(request.GET.get('start', 0)),
        "column_ordered": int(request.GET.get(columns[0], 0)),
        "type_order": request.GET.get(dirs[0], 'asc'),
        "search": request.GET.get('search[value]', ""),
        "searchable": searchable_cols,
        "month_wanted": request.GET.get("month", "none")
    }

    return params
