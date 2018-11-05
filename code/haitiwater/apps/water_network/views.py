from django.http import HttpResponse
from django.template import loader
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

from .classes.element_table import ElementTable, ElementFilter

from apps.water_network.models import Element
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('water_network.html')
    table = ElementTable(Element.objects.all(), template_name="components/tables/custom1.html")
    filter_set = ElementFilter(request.GET, queryset=Element.objects.all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'network_element': debug_fill_table(),
        'elements': filter_set.qs,
        'filter': filter_set,
    }
    return HttpResponse(template.render(context, request))


def debug_fill_table():
    table = []
    for i in range(1000):
        table.append({
                'id': 1,
                'type': 'Fontaine',
                'address': 'Rue du bois joli, 4',
                'users': 600,
                'state': "En service",
                'volume_m3': 10,
                'volume_gal': 2641.72,
            })
    return table
