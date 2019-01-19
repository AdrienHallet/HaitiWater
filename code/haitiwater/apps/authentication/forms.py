from django.contrib.auth.forms import PasswordChangeForm
from django import forms


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.PasswordInput()
    new_password1 = forms.PasswordInput
    new_password2 = forms.PasswordInput
