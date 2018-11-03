import django_filters
import django_tables2 as tables
from django_tables2.views import SingleTableMixin
import django_filters
from django_filters.views import FilterView
from django_filters import FilterSet

from ..models import Dummy


class DummyTable(tables.Table):
    export_formats = ['csv', 'xls', 'latex']
    name = tables.Column()
    class Meta:
        model = Dummy


class DummyFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Dummy
        fields = {"name"}


class FilteredDummyView(SingleTableMixin, FilterView):
    table_class = DummyTable
    model = Dummy
    template_name = 'components/tables/custom1.html'
    filterset_class = DummyFilter


