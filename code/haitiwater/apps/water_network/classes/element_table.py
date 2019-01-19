import django_tables2 as tables
from django_tables2.views import SingleTableMixin
import django_filters
from django_filters.views import FilterView
from django_filters import FilterSet

from ..models import Element


class ElementTable(tables.Table):
    id = tables.Column()
    name = tables.Column()
    type = tables.Column()
    location = tables.Column()

    export_formats = ['csv', 'xls', 'latex']

    class Meta:
        model = Element


class ElementFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Element
        fields = {"name"}


class FilteredElementView(SingleTableMixin, FilterView):

    model = Element
    table_class = ElementTable
    filterset_class = ElementFilter
    template_name = 'components/tables/custom1.html'


