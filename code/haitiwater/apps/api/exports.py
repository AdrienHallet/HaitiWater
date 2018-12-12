import re
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from ..water_network.models import Element, ElementType
from ..consumers.models import Consumer
import json


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
    all = []
    if d["table_name"] == "water_element":
        all_water_element = Element.objects.all()
        json_test["recordsTotal"] = len(all_water_element)
        if d["search"] == "":
            for elem in all_water_element:
                cust = Consumer.objects.filter(water_outlet=elem)
                tab = elem.network_descript()
                tab.insert(3, len(cust))
                all.append(tab)
        else:
            for elem in all_water_element:
                cust = Consumer.objects.filter(water_outlet=elem)
                tab = elem.network_descript()
                tab.insert(3, len(cust))
                for cols in d["searchable"]:
                    if cols < len(tab) and d["search"].lower() in str(tab[cols]).lower():
                        all.append(tab)
                        break

    elif d["table_name"] == "consumer":
        all_consumers = Consumer.objects.all()
        json_test["recordsTotal"] = len(all_consumers)
        if d["search"] == "":
            for elem in all_consumers:
                all.append(elem.descript())
        else:
            for elem in all_consumers:
                for cols in d["searchable"]:
                    tab = elem.descript()
                    if cols < len(tab) and d["search"].lower() in str(tab[cols]).lower():
                        all.append(tab)
                        break

    final = sorted(all, key=lambda x: x[d["column_ordered"]],
                   reverse=d["type_order"] != "asc")
    if d["length_max"] == -1:
        json_test["data"] = final
    else:
        json_test["data"] = final[d["start"]:d["start"]+d["length_max"]]
    json_test["recordsFiltered"] = len(final)
    return HttpResponse(json.dumps(json_test))

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        return add_network_element(request)
    elif element == "consumer":
        return add_consumer_element(request)
    else:
        return HttpResponse(status=500)

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
        return HttpResponse(status=404) #Outlet not found, can't create
    new_c = Consumer(last_name=last_name, first_name=first_name,
                          gender=gender, location=address, phone_number=phone,
                          email="", household_size=sub, water_outlet=outlet)
    new_c.save()
    return HttpResponse(status=200)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_network_element(request):
    type = request.POST.get("type", None).upper()
    loc = request.POST.get("localization", None)
    state = request.POST.get("state", None).upper()
    string_type = ElementType[type].value
    e = Element(name=string_type+" "+loc, type=type, status=state, location=loc) #Créer l'élément
    e.save()
    return HttpResponse(status=200)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def remove_element(request):
    print(request.POST)
    element = request.POST.get("table", None)
    if element == "water_element":
        id = request.POST.get("id", None)
        Element.objects.filter(id=id).delete()
        return HttpResponse(status=200)
    elif element == "consumer":
        id = request.POST.get("id", None)
        Consumer.objects.filter(id=id).delete()
        return HttpResponse({"draw": request.POST.get("draw", 0)+1}, status=200)
    return HttpResponse(status=500)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def edit_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        return edit_water_element(request)
    elif element == "consumer":
        return edit_consummer(request)
    else:
        return HttpResponse(status=500)


def edit_water_element(request):
    id = request.POST.get("id", None)
    elems = Element.objects.filter(id=id)
    if len(elems) < 0:
        return HttpResponse(status=404)
    elem = elems[0]
    elem.type = request.POST.get("type", None).upper()
    elem.location = request.POST.get("localization", None)
    elem.status = request.POST.get("state", None).upper()
    elem.save()
    return HttpResponse(status=200)


def edit_consummer(request):
    id = request.POST.get("id", None)
    consummers = Consumer.objects.filter(id=id)
    if len(consummers) < 0:
        return HttpResponse(status=404)
    consummer = consummers[0]
    consummer.first_name = request.POST.get("firstname", None)
    consummer.last_name = request.POST.get("lastname", None)
    consummer.gender = request.POST.get("gender", None)
    consummer.location = request.POST.get("address", None)
    consummer.household_size = request.POST.get("subconsumer", None)
    consummer.phone = request.POST.get("phone", None)
    outlet_id = request.POST.get("mainOutlet", None)
    outlet = Element.objects.filter(id=outlet_id)
    if len(outlet) > 0:
        outlet = outlet[0]
    else:
        return HttpResponse(status=404)  # Outlet not found, can't create
    consummer.water_outlet = outlet
    consummer.save()
    return HttpResponse(status=200)


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
