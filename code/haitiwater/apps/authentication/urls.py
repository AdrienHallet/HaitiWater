from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import forms
from . import views
from . import exports

urlpatterns = [
    url(r'^editer/changer-mot-de-passe/$', auth_views.PasswordChangeView.as_view(template_name='password.html'),
        name="change"),
    url(r'^editer/changer-mot-de-passe/fait/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_changed.html'), name="changedone"),
    path('editer/', views.profile, name='profile'),
    path('editer/infos/', exports.edit, name='profile'),
    path('', views.index, name='auth'),
]
