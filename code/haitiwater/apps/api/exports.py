from django.http import HttpResponse

def graph(request):
    export_format = request.GET.get('type', None)
    if export_format == "json":
        export_format = """{
               "jsonarray": [{
                  "name": "Joe",
                  "age": 12
               }, {
                  "name": "Tom",
                  "age": 14
               }]}"""
    return HttpResponse(export_format)