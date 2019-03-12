from django.db import models
from django.db.models import ManyToOneRel
from ..log.utils import *
from ..utils.common_models import *

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

    def infos(self):
        result = {}
        for field in Payment._meta.get_fields():
            if type(field) != ManyToOneRel:
                print(field.name)
                if field.name == "consumer":
                    result["Identifiant consommateur"] = self.consumer.id
                    result["Nom consommateur"] = self.consumer.first_name+" "+self.consumer.last_name
                elif field.name == "water_outlet":
                    result["Identifiant point d'eau"] = self.water_outlet.id
                    result["Nom point d'eau"] = self.water_outlet.name
                else:
                    result[field.verbose_name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)
