from django.contrib.gis.db import models
from ..water_network.models import Location, Element, ElementType


class Person(models.Model):

    first_name = models.CharField("Prénom", max_length=20)
    last_name = models.CharField("Nom", max_length=20)
    gender = models.CharField("Genre", max_length=1, choices=[("M", "Homme"), ("F", "Femme"), ("O", "Autre")], null=True)
    phone_number = models.CharField("Numéro de téléphone", max_length=10, null=True)
    email = models.CharField("Adresse email", max_length=50, null=True)
    #location = models.ForeignKey(Location, verbose_name="Localité", on_delete=models.CASCADE)
    location = models.CharField("Adresse", max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        abstract = True


class Consumer(Person):

    household_size = models.IntegerField("Taille du ménage")
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau", related_name="consumers", on_delete=models.CASCADE)
    #Consumer's zone is infered regarding the water_outlet he uses

    def descript(self):
        tab = [self.id, self.last_name, self.first_name, self.get_gender_display(),
               self.location, self.phone_number, self.household_size, self.water_outlet.name, ""]
        return tab