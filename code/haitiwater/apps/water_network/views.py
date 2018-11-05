from django.http import HttpResponse
from django.template import loader
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from .classes.water_element_table import DummyTable, DummyFilter
from apps.water_network.models import Dummy
from haitiwater.settings import PROJECT_VERSION, PROJECT_NAME


def index(request):
    template = loader.get_template('water_network.html')
    table = DummyTable(Dummy.objects.all(), template_name="components/tables/custom1.html")
    filter = DummyFilter(request.GET, queryset=Dummy.objects.all())
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    context = {
        'project_version': PROJECT_VERSION,
        'project_name': PROJECT_NAME,
        'dummy': filter.qs,
        'zone_name': "Nom de la zone",  # Todo Backend
        'filter': filter,
    }
    return HttpResponse(template.render(context, request))