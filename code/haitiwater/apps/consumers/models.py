from django.contrib.gis.db import models
from ..water_network.models import Location, Element


class Person(models.Model):

    first_name = models.CharField("Prénom", max_length=20)
    last_name = models.CharField("Nom", max_length=20)
    gender = models.CharField("Genre", max_length=1, choices=[("M", "Homme"), ("F", "Femme"), ("O", "Autre")], null=True)
    phoneNumber = models.CharField("Numéro de téléphone", max_length=10, null=True)
    email = models.CharField("Adresse email", max_length=50, null=True)
    location = models.ForeignKey(Location, verbose_name="Localité", on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        abstract = True


class Consumer(Person):

    household_size = models.IntegerField("Taille du ménage")
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau", related_name="consumers", on_delete=models.CASCADE)
