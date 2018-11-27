from django.urls import path

from . import views
from . import exports

urlpatterns = [
    path('', views.index, name='auth'),
    path('connect/', exports.connect, name='auth'),
]
