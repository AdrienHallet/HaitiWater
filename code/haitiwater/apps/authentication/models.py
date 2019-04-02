from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..utils.common_models import *
from ..water_network.models import Zone, Element


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField("Numéro de téléphone", max_length=10, null=True)
    zone = models.ForeignKey(Zone, verbose_name="Zone gérée", related_name="admins",
                             null=True, on_delete=models.CASCADE)
    outlets = ArrayField(models.CharField(max_length=30), blank=True, default=list, null=True)
    # Should be a ManyToManyField to Element, but refactor requires to dump DB

    def get_phone_number(self):
        return self.phone_number if self.phone_number is not None and self.phone_number != "0" else "Non spécifié"

    def infos(self):
        result = {
            "ID": self.id,
            "Identifiant": self.user.username,
            "Prénom": self.user.first_name,
            "Nom de famille": self.user.last_name,
            "Email": self.user.email,
            "Role": self.user.groups.values_list('name', flat=True)[0],
        }

        if self.zone:
            result["Zone gérée"] = self.zone.name
            result["_zone"] = self.zone.id
        elif len(self.outlets) > 0:
            all_outlets = ""
            for outlet_id in self.outlets:
                outlet = Element.objects.filter(id=outlet_id).first()
                if outlet is not None:
                    all_outlets += outlet.name + ", "
            result["Fontaines gérées"] = all_outlets[:-2]
            result["_outlets"] = self.outlets

        return result

    def log_add(self, transaction):
        add(self._meta.model_name, self.infos(), transaction)

    def log_delete(self, transaction):
        delete(self._meta.model_name, self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit(self._meta.model_name, self.infos(), old, transaction)

    def get_subordinates(self):
        sub = []
        for user in User.objects.all():
            if user.username == "admin":  # Skip the admin
                pass
            elif user.profile.zone is not None:  # Zone manager
                if user.profile.zone.name in self.zone.subzones and user.username != self.user.username:
                    sub.append(user)
            elif len(user.profile.outlets) > 0:  # Fountain manager
                to_add = True
                for outlet_id in user.profile.outlets:
                    outlet = Element.objects.filter(id=outlet_id).first()
                    if outlet is not None and outlet.zone.name not in self.zone.subzones:
                        to_add = False
                if to_add:
                    sub.append(user)
        return sub

    def get_zone(self):
        if self.zone:
            return self.zone.name
        else:
            outlet = Element.objects.filter(id=self.outlets[0])
            if len(outlet) != 1:
                return ""
            outlet = outlet[0]
            higher_zone =  outlet.zone
            for elem in self.outlets[1:]:
                outlet = Element.objects.filter(id=elem)
                if len(outlet) != 1:
                    return ""
                outlet = outlet[0]
                other_zone = outlet.zone
                if higher_zone.name in other_zone.subzones and other_zone.name not in higher_zone.subzones:
                    higher_zone = other_zone
            return higher_zone.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    raw = kwargs.get('raw', False)
    if not raw:
        if created:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    raw = kwargs.get('raw', False)
    if not raw:
        instance.profile.save()
