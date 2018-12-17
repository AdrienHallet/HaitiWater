from django.contrib.gis.db import models
from ..water_network.models import Element

# Create your models here.
class Report(models.Model):
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau concernée",
                                     related_name="reports", on_delete=models.CASCADE)
    month = models.CharField("Mois", max_length=10, choices=[("January", "Janvier"),
                                                             ("February", "Février"),
                                                             ("March", "Mars"),
                                                             ("April", "Avril"),
                                                             ("May", "Mai"),
                                                             ("June", "Juin"),
                                                             ("July", "Juillet"),
                                                             ("August", "Août"),
                                                             ("September", "Septembre"),
                                                             ("October", "Octobre"),
                                                             ("December", "Décembre")], null=False)
    year = models.IntegerField("Année")
    was_active = models.BooleanField("A été active")
    quantity_distributed = models.IntegerField("Quantité distribuée")
    price = models.IntegerField("Prix au mètre cube")
    recette = models.IntegerField("Recettes du mois")


class Ticket(models.Model):
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau concernée",
                                     related_name="tickets_open", on_delete=models.CASCADE)
    comment = models.CharField("Commentaire", max_length=500, null=True)
    urgency = models.CharField("Niveau d'urgence", max_length=10, choices=[("low", "Bas"),
                                                             ("middle", "Moyen"),
                                                             ("high", "Haut")])
    type = models.CharField("Type de panne", max_length=10, choices=[("mechanical", "Mécanique"),
                                                                           ("quality", "Qualité"),
                                                                           ("other", "Autre")])
    image = models.BinaryField("Image", null=True)
