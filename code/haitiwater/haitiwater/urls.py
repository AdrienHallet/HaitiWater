"""haitiwater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.authentication.urls')),
    path('accueil/', include('apps.dashboard.urls')),
    path('reseau/', include('apps.water_network.urls')),
    path('consommateurs/', include('apps.consumers.urls')),
    path('rapport/', include('apps.report.urls')),
    path('gestion/', include('apps.zone_management.urls')),
    path('api/', include('apps.api.urls')),
    path('user/', include('apps.authentication.urls')),
    path('offline/', include('apps.offline.urls')),
    url(r'^sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js')
]
# https://stackoverflow.com/questions/38696595/django-and-service-workers-serve-sw-js-at-applications-root-url
