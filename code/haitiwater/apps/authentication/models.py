from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from ..water_network.models import Zone
from ..utils.common_models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, verbose_name="Zone gérée",
                             related_name="admins", null=True, on_delete=models.CASCADE)

    outlets = ArrayField(models.CharField(max_length=30), blank=True, default=list, null=True)

    def infos(self):
        result = {}
        result["identifiant"] = self.user.username
        result["first_name"] = self.user.first_name
        result["last_name"] = self.user.last_name
        result["email"] = self.user.email
        result["role"] = self.user.groups
        for field in Profile._meta.get_fields():
            result[field.name] = self.__getattribute__(field.name)
        print("Infos")
        print(result)
        return result

    def log_add(self, transaction):
        print(self.infos())
        add("User", self.infos(), transaction)

    def log_delete(self, transaction):
        delete("User", self.infos(), transaction)

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
