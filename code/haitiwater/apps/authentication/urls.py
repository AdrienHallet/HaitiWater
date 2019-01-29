from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from . import forms
from . import views
from . import exports


# views.py
class LoginAfterPasswordChangeView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy('login')

login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view(template_name='password.html'))

urlpatterns = [
    url(r'^editer/changer-mot-de-passe/$', login_after_password_change,
        name="change"),
    path('editer/', views.profile, name='profile'),
    path('editer/infos/', exports.edit, name='profile'),
    path('', views.index, name='auth'),
]
