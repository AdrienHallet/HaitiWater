import os

from django.contrib.gis.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from ..water_network.models import Element
from ..utils.common_models import *
from enum import Enum


class UrgencyType(Enum):
    LOW = "Bas"
    MEDIUM = "Moyen"
    HIGH = "Haut"


class BreakType(Enum):
    MECHANICAL = "Mécanique"
    QUALITY = "Qualité"
    OTHER = "Autre"


class StatusType(Enum):
    UNRESOLVED = "Non résolu"
    RESOLVED = "Résolu"
    CURRENT = "En cours de résolution"


class Month(Enum):
    January = "Janvier"
    February = "Février"
    March = "Mars"
    April = "Avril"
    May = "Mai"
    June = "Juin"
    July = "Juillet"
    August = "Août"
    September = "Septembre"
    October = "Octobre"
    December = "Décembre"


# Create your models here.
class Report(models.Model):
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau concernée",
                                     related_name="reports", on_delete=models.CASCADE)
    timestamp = models.DateTimeField("Date de soummission", auto_now_add=True)
    has_data = models.BooleanField("A un compteur", default=False)
    was_active = models.BooleanField("A été active", default=False)
    days_active = models.IntegerField("Jours d'activité", null=False, default=0)
    hours_active = models.IntegerField("Heures d'activité", null=False, default=0)
    quantity_distributed = models.FloatField("Quantité distribuée", null=True)
    price = models.FloatField("Prix au mètre cube", null=True)
    recette = models.FloatField("Recettes du mois", null=True)  # TODO English please x)

    def infos(self):
        result = {}
        for field in Report._meta.get_fields():
            if field.name == "has_data" and self.was_active:
                result[field.verbose_name] = "Oui" if self.has_data else "Non"
                result["_has_data"] = self.has_data
            elif field.name == "was_active":
                result[field.verbose_name] = "Oui" if self.was_active else "Non"
                result["_has_data"] = self.was_active
            elif field.name == "timestamp":
                result[field.verbose_name] = str(self.timestamp.date())
            else:
                result[field.verbose_name] = self.__getattribute__(field.name)

        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)


class Ticket(models.Model):
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau concernée",
                                     related_name="tickets_open", on_delete=models.CASCADE)
    comment = models.CharField("Commentaire", max_length=500, null=True)
    urgency = models.CharField("Niveau d'urgence", max_length=10, choices=[(i.name, i.value) for i in UrgencyType])
    type = models.CharField("Type de panne", max_length=10, choices=[(i.name, i.value) for i in BreakType])
    image = models.ImageField("Image", upload_to="ticket_images", null=True) #This saves the image to server. We'll see if it stays
    status = models.CharField("Etat de résolution", max_length=10, choices=[(i.name, i.value) for i in StatusType],
                              default="UNRESOLVED")

    def descript(self):
        return [self.id, self.get_urgency(),
                self.water_outlet.name, self.get_break(),
                self.comment, self.get_status(), self.get_image()]

    def get_urgency(self):
        return UrgencyType[self.urgency].value

    def get_break(self):
        return BreakType[self.type].value

    def get_status(self):
        return StatusType[self.status].value

    def get_image(self):
        return self.image.url if self.image else None

    def infos(self):
        result = {}
        for field in Ticket._meta.get_fields():
            if field.name == "water_outlet":
                result[field.verbose_name] = self.water_outlet.id
                result["Nom de la sortie d'eau"] = self.water_outlet.name
            elif field.name == "urgency":
                result[field.verbose_name] = self.get_urgency()
                result["_urgency"] = self.urgency
            elif field.name == "status":
                result[field.verbose_name] = self.get_status()
                result["_status"] = self.status
            elif field.name == "type":
                result[field.verbose_name] = self.get_break()
                result["_type"] = self.type
            else:
                result[field.verbose_name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)

@receiver(post_delete, sender=Ticket)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
