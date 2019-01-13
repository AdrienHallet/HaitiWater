from django.conf.urls import url

from . import exports

urlpatterns = [
    url(r'graph/$', exports.graph, name='graph'),
    url(r'table/$', exports.table, name='table'),
    url(r'add/$', exports.add_element, name='add'),
    url(r'remove/$', exports.remove_element, name='remove'),
    url(r'edit/$', exports.edit_element, name='edit'),
    url(r'report/$', exports.add_report_element, name='report_add'),
]
