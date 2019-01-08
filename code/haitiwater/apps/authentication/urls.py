from django.urls import path

from . import views
from . import exports

urlpatterns = [
    path('connect/', exports.connect, name='auth'),
    path('editer/', views.profile, name='profile'),
    path('', views.index, name='auth'),
]
