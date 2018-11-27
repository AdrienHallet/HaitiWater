import re
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from ..water_network.models import Element
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
               }]}"""
        json_val = json.loads(export)
        all_consumers = Consumer.objects.all()
        for elem in all_consumers:
            if elem.gender == "M" or elem.gender == "Homme":
                json_val['jsonarray'][1]['data'] += 1 #One more man
            else:
                json_val['jsonarray'][0]['data'] += 1 #One more women
    return HttpResponse(json.dumps(json_val))


def table(request):
    # Todo backend https://datatables.net/manual/server-side
    # Note that "editable" is a custom field. Setting it to true displays the edit/delete buttons.
    export = """{
                      "editable": true,
                      "draw": 2,
                      "recordsTotal": 100,
                      "recordsFiltered": 100,
                      "data": []
                    }"""
    json_test = json.loads(export)
    json_test["draw"] = str(int(request.GET.get('draw', "1")) + 1)
    d = parse(request)
    all = []
    if d["table_name"] == "water_element":
        all_water_element = Element.objects.all()
        for elem in all_water_element[d["start"]:d["start"]+d["length_max"]]:
            cust = Consumer.objects.filter(water_outlet=elem)
            tab = elem.network_descript()
            tab.insert(3, len(cust))
            all.append(tab)

    elif d["table_name"] == "consumer":
        all_consumers = Consumer.objects.all()
        for elem in all_consumers[d["start"]:d["start"] + d["length_max"]]:
            all.append(elem.descript())
    final = sorted(all, key=lambda x: x[d["column_ordered"]],
                   reverse=d["type_order"] != "asc")
    json_test["data"] = final
    return HttpResponse(json.dumps(json_test))


@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_network_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        type = request.POST.get("type", None).upper()
        loc = request.POST.get("localization", None)
        state = request.POST.get("state", None).upper()
        e = Element(name="", type=type, status=state, location=loc) #Créer l'élément
        e.save()
        return HttpResponse(status=200)
    elif element == "consumer":
        print("Hello")

    return HttpResponse(status=500)

@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def remove_network_element(request):
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
def edit_network_element(request):
    element = request.POST.get("table", None)
    if element == "water_element":
        id = request.POST.get("id", None)
        elems = Element.objects.filter(id=id)
        elem = elems[0]
        elem.type = request.POST.get("type", None).upper()
        elem.location = request.POST.get("localization", None)
        elem.status = request.POST.get("state", None).upper()
        elem.save()
        return HttpResponse(status=200)

    return HttpResponse(status=500)


def parse(request):
    test = re.compile('order\[\d*\]\[dir\]')
    res = list(filter(test.match, dict(request.GET).keys()))
    d = {"table_name": request.GET.get('name', None),
         "length_max": int(request.GET.get('length', 10)),
         "start": int(request.GET.get('start', 0)),
         "column_ordered": int(re.search('order\[(\d*)\]\[dir\]', res[0]).group(1)),
         "type_order": request.GET.get(res[0], 'asc')
         }
    return d
