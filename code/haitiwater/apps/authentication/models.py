from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from ..water_network.models import Zone, Element
from ..utils.common_models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, verbose_name="Zone gérée",
                             related_name="admins", null=True, on_delete=models.CASCADE)

    outlets = ArrayField(models.CharField(max_length=30), blank=True, default=list, null=True)

    def infos(self):
        result = {}
        result["Identifiant"] = self.user.username
        result["Prénom"] = self.user.first_name
        result["Nom de famille"] = self.user.last_name
        result["Email"] = self.user.email
        result["Role"] = self.user.groups.values_list('name',flat=True)[0]
        for field in Profile._meta.get_fields():
            result[field.verbose_name] = self.__getattribute__(field.name)
            if field.name == "zone" and self.zone:
                result[field.verbose_name] = self.zone.id
        return result

    def log_add(self, transaction):
        add("User", self.infos(), transaction)

    def log_delete(self, transaction):
        delete("User", self.infos(), transaction)

    def log_edit(self, old, transaction):
        edit("User", self.infos(), old, transaction)

    def get_subordinates(self):
        sub = []
        all_users = User.objects.all()
        for user in all_users:
            if not user.profile:
                pass
            elif user.profile.zone != None: #Zone manager
                if user.profile.zone.name in self.zone.subzones \
                        and user != self.user:
                    sub.append(user)
            elif len(user.profile.outlets) > 0: #Fountain manager
                add = True
                for outlet in user.profile.outlets:
                    outlet = Element.objects.filter(id=outlet)[0]
                    if outlet.zone.name not in self.zone.subzones:
                        add = False
                if add:
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
