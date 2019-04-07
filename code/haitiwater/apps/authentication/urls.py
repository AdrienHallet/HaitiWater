from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, reverse_lazy

from . import exports
from . import views


class LoginAfterPasswordChangeView(PasswordChangeView):

    @property
    def success_url(self):
        return reverse_lazy('login')


login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view(template_name='profile.html'))

urlpatterns = [
    url(r'^editer/$', login_after_password_change, name="change"),
    path('editer/infos/', exports.edit, name='profile'),
    path('', views.index, name='auth'),
]
