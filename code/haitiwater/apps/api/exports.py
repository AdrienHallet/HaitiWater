from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from ..water_network.models import Element
from ..consumers.models import Consumer
import json


def graph(request):
    export_format = request.GET.get('type', None)
    if export_format == "consumer_sex_pie":
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
    table_name = request.GET.get('name', None)
    if table_name == "water_element":
        all_water_element = Element.objects.all() #TODO : this is ugly, talk with front-end
        export = """{
                  "editable": true,
                  "draw": 2,
                  "recordsTotal": 100,
                  "recordsFiltered": 100,
                  "data": []
                }"""
        json_test = json.loads(export)
        id = 1
        for elem in all_water_element:
            cust = Consumer.objects.filter(water_outlet=elem)
            tab = elem.network_descript()
            tab.insert(0, str(id))
            tab.insert(3, len(cust))
            json_test['data'].append(tab)
            id += 1

    return HttpResponse(json.dumps(json_test))


@csrf_exempt #TODO : this is a hot fix for something I don't understand, remove to debug
def add_network_element(request):
    print(request.POST.getlist('key'))
    e = Element() #Créer l'élément

    return HttpResponse()

