from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from enum import Enum
from django.contrib.postgres.fields import ArrayField
from django.db.models import ManyToOneRel
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    # Réservoir
    TANK = "Réservoir"


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
    fountain_price = models.FloatField("Prix de la souscription à une fontaine")
    fountain_duration = models.IntegerField("Durée en mois de la souscription à une fontaine")
    kiosk_price = models.FloatField("Prix de la souscription à un kiosque")
    kiosk_duration = models.IntegerField("Durée en mois de la souscription à un kiosque")
    superzone = models.ForeignKey('self', verbose_name="Superzone", related_name='sub', null=True, on_delete=models.CASCADE)
    subzones = ArrayField(models.CharField(max_length=30), blank=True, default=list)

    # Generated : subzones, locations

    def __str__(self):
        return self.name

    def descript(self):
        return [self.id, self.name, self.fountain_price, self.fountain_duration, self.kiosk_price, self.kiosk_duration]

    def infos(self):
        result = {
            "Zone mère": str(self.superzone.id)+" ("+self.superzone.name+")" if self.superzone else "Aucune",
            "Nom": self.name,
            "ID": self.id,
            "Prix des fontaines": self.fountain_price,
            "Durée de la souspricption des fontaines": self.fountain_duration,
            "Prix des kiosques": self.kiosk_price,
            "Durée de la souspricption des kiosques": self.kiosk_duration,
        }
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)


class VirtualZoneTotal(models.Model):
    relevant_model = models.BigIntegerField("Id", primary_key=True)
    zone_name = models.CharField("Nom de la zone", max_length=300)
    indiv_consumers = models.IntegerField("Consommateurs individuels de cette zone", null=False, default=0)
    total_consumers = models.IntegerField("Consommateurs de cette zone", null=False, default=0)
    fountains = models.IntegerField("Fontaines de cette zone", null=False, default=0)
    kiosks = models.IntegerField("Kiosques de cette zone", null=False, default=0)
    indiv_outputs = models.IntegerField("Prises individuelles de cette zone", null=False, default=0)
    water_points = models.IntegerField("Sources de cette zone", null=False, default=0)
    pipes = models.IntegerField("Conduites de cette zone", null=False, default=0)
    tanks = models.IntegerField("Réservoirs de cette zone", null=False, default=0)

    class Meta:
        managed = False
        db_table = 'water_network_virtualzonetotal'


class Element(models.Model):

    name = models.CharField("Nom", max_length=50)
    type = models.CharField("Type", max_length=20, choices=[(i.name, i.value) for i in ElementType])
    status = models.CharField("État", max_length=20, choices=[(i.name, i.value) for i in ElementStatus])
    zone = models.ForeignKey(Zone, verbose_name="Zone de l'élément", related_name="elements", on_delete=models.CASCADE, default=1)
    location = models.CharField("Localisation", max_length=500)
    manager_names = models.CharField("Nom des gestionnaires", max_length=300, default="Pas de gestionnaire")

    def __str__(self):
        return self.name

    def is_in_subzones(self, zone):
        return self.zone.name in zone.subzones

    def get_type(self):
        return ElementType[self.type].value

    def get_status(self):
        return ElementStatus[self.status].value

    def get_consumers(self):
        from ..consumers.models import Consumer #Avoid cycle in imports
        consumers = Consumer.objects.filter(water_outlet_id=self.id)
        total = 0
        for consumer in consumers:
            total += consumer.household_size + 1
        return total

    def get_current_output(self):
        from ..report.models import Report #Avoid cycle in imports
        from datetime import date
        reports = Report.objects.filter(water_outlet_id=self.id,
                                        timestamp__month=date.today().month,
                                        has_data=True,
                                        was_active=True)
        if len(reports) > 1:
            return "Erreur dans le calcul de quantité"
        elif len(reports) == 0:
            return 0
        else:
            return reports[0].quantity_distributed

    def get_all_output(self):
        from ..report.models import Report  # Avoid cycle in imports
        reports = Report.objects.filter(water_outlet_id=self.id, has_data=True, was_active=True)
        if len(reports) == 0:
            return 0, 0
        total = 0
        for report in reports:
            total += report.quantity_distributed
        return total, total/len(reports)

    def get_managers(self):
        all_managers = User.objects.all()
        result = ""
        for user in all_managers:
            if user.profile.outlets:
                if str(self.id) in user.profile.outlets:
                    result += user.first_name + " " + user.last_name + ", "
        if result == "":
            result = "Pas de gestionnaire  "
        return result[:-2]

    def get_price_and_duration(self):
        price = 0
        duration = 1
        if self.type == ElementType.FOUNTAIN.name:
            price = self.zone.fountain_price
            duration = self.zone.fountain_duration
        elif self.type == ElementType.KIOSK.name:
            price = self.zone.kiosk_price
            duration = self.zone.kiosk_duration
        return price, duration

    def network_descript(self):
        self.manager_names = self.get_managers()
        self.save()
        view = VirtualElementTotal.objects.get(relevant_model=self.id)
        tab = [self.id, self.get_type(), self.location, view.total_consumers,
               self.get_status(), round(view.total_distributed, 2),
               round(view.total_distributed * 264.17, 2), self.manager_names, self.zone.name]
        return tab

    def infos(self):
        result = {}
        for field in Element._meta.get_fields():
            if type(field) != ManyToOneRel:
                if field.name == "zone":
                    result[field.verbose_name] = self.zone.name
                    result["_zone"] = self.zone.id
                if field.name == "type":
                    result["Type"] = ElementType[self.type].value #Not working wtf
                    result["_type"] = self.type
                if field.name == "status":
                    result[field.verbose_name] = self.get_status()
                    result["_status"] = self.status
                else:
                    result[field.verbose_name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)



class VirtualElementTotal(models.Model):
    relevant_model = models.BigIntegerField("Id", primary_key=True)
    total_distributed = models.FloatField("Volume total distribué", null=False, default=0)
    total_consumers = models.IntegerField("Consommateurs de cet élément", null=False, default=0)

    class Meta:
        managed = False
        db_table = 'water_network_virtualelementtotal'


class Location(models.Model):

    elem = models.ForeignKey(Element, verbose_name="Elément représenté", related_name="locations", on_delete=models.CASCADE)
    lon = models.FloatField("Longitude")
    lat = models.FloatField("Latitude")
    json_representation = JSONField(verbose_name="GeoJSON", null=True)
    poly = models.GeometryField("Polygone", null=True)

    # Generated : elements
    def __str__(self):
        return self.elem.name + " : (" + str(self.lon) + ", " + str(self.lat) + ")"

    def infos(self):
        result = {
            "ID": self.id,
            "Nom de l'élément": self.elem.name,
            "Identifiant de l'élément": self.elem.id,
            "Latitude": self.lat,
            "Longitude": self.lon,
            "_json": self.json_representation,
            "_poly": self.poly
        }
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)

