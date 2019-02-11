from django.contrib.auth.models import User
from django.contrib.gis.db import models
from enum import Enum
from django.contrib.postgres.fields import ArrayField
from django.db.models import ManyToOneRel

from ..utils.common_models import *

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
    PIPE = "Conduite"


class ElementStatus(Enum):
    OK = "En service"
    REPAIR = "Nécessite réparation"
    REPAIRING = "En réparation"
    URGENT = "Hors service (Urgent)"
    KO = "Hors service"


##########
# Models #
##########


class Zone(models.Model):

    name = models.CharField("Nom", max_length=50)
    superzone = models.ForeignKey('self', verbose_name="Superzone", related_name='sub', null=True, on_delete=models.CASCADE)
    subzones = ArrayField(models.CharField(max_length=30), blank=True, default=list)

    # Generated : subzones, locations

    def __str__(self):
        return self.name

    def descript(self):
        return [self.id, self.name]

    def infos(self):
        result = {}
        for field in Zone._meta.get_fields():
            if field.name == "superzone":
                result[field.name] = self.superzone.id
            else:
                result[field.name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add("Zone", self.infos(), transaction)

    def log_delete(self, transaction):
        delete("Zone", self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit("Zone", self.infos(), old, transaction)


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
    zone = models.ForeignKey(Zone, verbose_name="Zone de l'élément", related_name="elements", on_delete=models.CASCADE, default=1)
    location = models.CharField("Localisation", max_length=50)

    def __str__(self):
        return self.name

    def is_in_subzones(self, zone):
        return self.zone.name in zone.subzones

    def get_managers(self):
        all_managers = User.objects.all()
        result = ""
        for user in all_managers:
            if user.profile.outlets:
                if str(self.id) in user.profile.outlets:
                    result += user.username+", "
        if result == "":
            result = "Pas de gestionnaire  "
        return result[:-2]

    def network_descript(self):
        tab = [self.id, ElementType[self.type].value, self.location,
               ElementStatus[self.status].value, self.get_managers(), self.zone.name]
        return tab

    def infos(self):
        result = {}
        for field in Element._meta.get_fields():
            if type(field) != ManyToOneRel:
                if field.name == "zone":
                    result[field.verbose_name] = self.zone.id
                else:
                    result[field.verbose_name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add("WaterElement", self.infos(), transaction)

    def log_delete(self, transaction):
        delete("WaterElement", self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit("WaterElement", self.infos(), old, transaction)
