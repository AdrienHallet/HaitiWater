from django.db import models
from ..consumers.models import Consumer
from ..water_network.models import Element


class Invoice(models.Model):

    consumer = models.ForeignKey(Consumer, verbose_name="Consommateur",
                                 related_name="invoices", on_delete=models.CASCADE)
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau",
                                     related_name="invoices", on_delete=models.CASCADE)
    creation = models.DateField("Date de la facture", auto_now=True)
    expiration = models.DateField("Date d'expiration de la souscription")
    amount = models.FloatField("Montant")


class Payment(models.Model):

    consumer = models.ForeignKey(Consumer, verbose_name="Consommateur",
                                 related_name="payments", on_delete=models.CASCADE)
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau",
                                     related_name="payments", on_delete=models.CASCADE)
    date = models.DateField("Date de la facture", auto_now=True)
    amount = models.FloatField("Montant")

    def descript(self):
        return [self.id, str(self.date), self.amount, self.water_outlet.name]
