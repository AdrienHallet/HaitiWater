from django.http import HttpResponse


def graph(request):
    export_format = request.GET.get('type', None)
    if export_format == "consumer_sex_pie":
        export_format = """{
               "jsonarray": [{
                  "label": "Femmes",
                  "data": 550
               }, {
                  "label": "Hommes",
                  "data": 450
               }]}"""
    return HttpResponse(export_format)


def table(request):
    # Todo backend https://datatables.net/manual/server-side
    # Note that "editable" is a custom field. Setting it to true displays the edit/delete buttons.
    table_name = request.GET.get('name', None)
    if table_name == "water_element":
        export = """{
                  "editable": true,
                  "draw": 2,
                  "recordsTotal": 100,
                  "recordsFiltered": 100,
                  "data": [
                    [
                      "1",
                      "Fontaine",
                      "Centre machin truc",
                      "600",
                      "En service",
                      "x",
                      "y"
                    ],
                    [
                      "2",
                      "Fontaine",
                      "Centre machin truc",
                      "600",
                      "En service",
                      "x",
                      "y"
                    ]
                  ]
                }"""
    return HttpResponse(export)

