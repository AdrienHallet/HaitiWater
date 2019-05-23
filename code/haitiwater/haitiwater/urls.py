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
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login/'), name='login_redirect'),
    path('admin/', admin.site.urls),
    path('accueil/', include('apps.dashboard.urls')),
    path('reseau/', include('apps.water_network.urls')),
    path('consommateurs/', include('apps.consumers.urls')),
    path('rapport/', include('apps.report.urls')),
    path('gestion/', include('apps.zone_management.urls')),
    path('historique/', include('apps.log.urls')),
    path('api/', include('apps.api.urls')),
    path('profil/', include('apps.authentication.urls')),
    path('user/', include('apps.authentication.urls')),  # TODO Why two ?
    path('offline/', include('apps.offline.urls')),
    path('aide/', include('apps.help.urls')),
    path('finances/', include('apps.financial.urls')),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='authentication.html'),
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),
    url(r'^login/recuperer-mot-de-passe/$',
        auth_views.PasswordResetView.as_view(template_name="password-reset.html"),
        name="reset"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-confirm.html"),
        name='password_reset_confirm'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="password-reset-done.html"),
        name='password_reset_done'),
    url(r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"),
        name='password_reset_complete'),
]

# https://stackoverflow.com/questions/38696595/django-and-service-workers-serve-sw-js-at-applications-root-url
urlpatterns += [
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
]
