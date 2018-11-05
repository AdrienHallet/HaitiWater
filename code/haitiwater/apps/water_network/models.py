from django.contrib.gis.db import models
from enum import Enum


#########
# Enums #
#########

# https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63


class ElementType(Enum):
    # Entrée d'eau
    SOURCE = "Source"
    # Sortie d'eau
    FOUNTAIN = "Fontaine"
    KIOSK = "Kiosque"
    INDIVIDUAL = "Prise individuelle"
    # Conduite
    PIPE = "Tuyau"


class ElementStatus(Enum):
    OK = "En service"
    REPAIR = "En réparation"
    URGENT = "Hors service (Urgent)"
    KO = "Hors service"


##########
# Models #
##########


class Zone(models.Model):

    name = models.CharField("Nom", max_length=50)
    superzone = models.ForeignKey('self', verbose_name="Superzone", related_name='subzones', null=True, on_delete=models.CASCADE)
    # TODO see if ManyToMany ?

    # Generated : subzones, locations

    def __str__(self):
        return self.name


class Location(models.Model):

    zone = models.ForeignKey(Zone, verbose_name="Zone", related_name="locations", on_delete=models.CASCADE)
    lon = models.FloatField("Longitude")
    lat = models.FloatField("Latitude")
    poly = models.MultiPolygonField("Multi-polygone", null=True)

    # Generated : elements

    def __str__(self):
        return self.zone.name + " : (" + str(self.lon) + ", " + str(self.lat) + ")"


class Element(models.Model):

    name = models.CharField("Nom", max_length=50)
    type = models.CharField("Type", max_length=20, choices=[(i.name, i.value) for i in ElementType])
    status = models.CharField("État", max_length=20, choices=[(i.name, i.value) for i in ElementStatus])
    location = models.ForeignKey(Location, verbose_name="Localité", related_name="elements", on_delete=models.CASCADE)

    def __str__(self):
        return self.name