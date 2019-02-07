from django.contrib.auth.models import User
from django.contrib.gis.db import models
from enum import Enum
from django.contrib.postgres.fields import ArrayField

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

    def get_manager(self):
        managers = User.objects.all()
        for manager in managers:
            if str(self.id) in manager.profile.outlets:
                return manager.username

    def get_consumers(self):
        from ..consumers.models import Consumer #Avoid cycle in imports
        consumers = Consumer.objects.filter(water_outlet_id=self.id)
        total = 0
        for consumer in consumers:
            total += consumer.household_size + 1
        return total

    def get_current_output(self):
        from ..report.models import Report #Avoid cycle in imports
        from ..utils.get_data import get_current_month
        reports = Report.objects.filter(water_outlet_id=self.id,
                                        month=get_current_month().upper())
        if len(reports) > 1:
            return "Erreur dans le calcul de quantité"
        elif len(reports) == 0:
            return 0
        else:
            return reports[0].quantity_distributed

    def get_all_output(self):
        from ..report.models import Report  # Avoid cycle in imports
        reports = Report.objects.filter(water_outlet_id=self.id)
        total = 0
        for report in reports:
            total += report.quantity_distributed
        return total, total/len(reports)


    def network_descript(self):
        tab = [self.id, ElementType[self.type].value, self.location,
               ElementStatus[self.status].value]
        return tab
