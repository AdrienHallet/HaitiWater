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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='login/'), name='login_redirect'),
    url(r'^accueil/$', include('apps.dashboard.urls')),
    path('reseau/', include('apps.water_network.urls')),
    path('consommateurs/', include('apps.consumers.urls')),
    path('rapport/', include('apps.report.urls')),
    path('gestion/', include('apps.zone_management.urls')),
    path('api/', include('apps.api.urls')),
    path('profil/', include('apps.authentication.urls')),

]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='authentication.html'),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),  name='logout'),
    url(r'^login/recuperer-mot-de-passe/$', auth_views.PasswordResetView.as_view(), name="reset"),
    url(r'^admin/', admin.site.urls),
]
