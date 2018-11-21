from django.db import models

from ..consumers.models import Person


class Authentication(Person):

    identifiant = models.CharField("Identifiant", max_length=20)
    password = models.CharField("Mot de passe", max_length=30)
