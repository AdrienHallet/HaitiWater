from django.contrib.gis.db import models
from django.db.models import ManyToOneRel

from ..log.utils import *
from ..utils.common_models import *
from ..water_network.models import Location, Element


class Consumer(models.Model):

    first_name = models.CharField("Prénom", max_length=20)
    last_name = models.CharField("Nom", max_length=20)
    gender = models.CharField("Genre", max_length=1, choices=[("M", "Homme"), ("F", "Femme"), ("O", "Autre")], null=True)
    phone_number = models.CharField("Numéro de téléphone", max_length=10, null=True)
    location = models.CharField("Adresse", max_length=50)
    household_size = models.IntegerField("Taille du ménage")
    water_outlet = models.ForeignKey(Element, verbose_name="Sortie d'eau", related_name="consumers", on_delete=models.CASCADE)
    creation_date = models.DateTimeField("Date de création", auto_now_add=True)
    # Consumer's zone is infered regarding the water_outlet he uses

    def __str__(self):
        return self.first_name + " " + self.last_name

    def descript(self):
        view = VirtualConsumersBalance.objects.filter(relevant_model=self.id).first()
        tab = [self.id, self.last_name, self.first_name, self.get_gender_display(),
               self.location, self.get_phone_number(),
               self.household_size, self.water_outlet.name, view.balance, self.water_outlet.zone.name]
        return tab

    def get_phone_number(self):
        return self.phone_number if self.phone_number != "0" else "Non spécifié"

    def infos(self):
        result = {}
        for field in Consumer._meta.get_fields():
            if type(field) != ManyToOneRel:
                if field.name == "water_outlet":
                    result[field.verbose_name] = self.water_outlet.name
                    result["_water_outlet"] = self.water_outlet_id
                elif field.name == "gender":
                    result[field.verbose_name] = self.get_gender_display()
                    result["_gender"] = self.gender
                elif field.name == "phone_number":
                    result[field.verbose_name] = self.get_phone_number()
                elif field.name == "creation_date":
                    result[field.verbose_name] = str(self.creation_date.date())
                else:
                    result[field.verbose_name] = self.__getattribute__(field.name)
        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)


class VirtualConsumersBalance(models.Model):
    relevant_model = models.BigIntegerField("Id", primary_key=True)
    balance = models.FloatField("Balance", null=False, default=0)

    class Meta:
        managed = False
        db_table = 'consumer_virtualtotalbalance'
