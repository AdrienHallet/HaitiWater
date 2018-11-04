from django.http import HttpResponse

def graph(request):
    export_format = request.GET.get('type', None)
    if export_format == "json1":
        export_format = """{
               "jsonarray": [{
                  "name": "Joe",
                  "age": 12
               }, {
                  "name": "Tom",
                  "age": 14
               }]}"""
    if export_format == "json2":
        export_format = """{
               "jsonarray": [{
                  "name": "Joe",
                  "age": 16
               }, {
                  "name": "Tom",
                  "age": 14
               }]}"""
    return HttpResponse(export_format)