from django.contrib.gis.db import models
from ..water_network.models import Element
from enum import Enum


class UrgencyType(Enum):
    LOW = "Bas"
    MEDIUM = "Moyen"
    HIGH = "Haut"


class BreakType(Enum):
    MECHANICAL = "Mécanique"
    QUALITY = "Qualité"
    OTHER = "Autre"


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
    month = models.CharField("Mois", max_length=10, choices=[(i.name, i.value) for i in Month], null=False)
    year = models.IntegerField("Année")
    was_active = models.BooleanField("A été active")
    quantity_distributed = models.FloatField("Quantité distribuée")
    price = models.FloatField("Prix au mètre cube")
    recette = models.FloatField("Recettes du mois")


class Ticket(models.Model):
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau concernée",
                                     related_name="tickets_open", on_delete=models.CASCADE)
    comment = models.CharField("Commentaire", max_length=500, null=True)
    urgency = models.CharField("Niveau d'urgence", max_length=10, choices=[(i.name, i.value) for i in UrgencyType])
    type = models.CharField("Type de panne", max_length=10, choices=[(i.name, i.value) for i in BreakType])
    image = models.ImageField("Image", null=True) #This saves the image to server. We'll see if it stays

    def descript(self):
        return [self.id, "", UrgencyType[self.urgency].value,
                self.water_outlet.name, BreakType[self.type].value,
                self.comment, ""]
