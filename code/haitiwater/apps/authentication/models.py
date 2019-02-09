from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from ..water_network.models import Zone, Element

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, verbose_name="Zone gérée",
                             related_name="admins", null=True, on_delete=models.CASCADE)

    outlets = ArrayField(models.CharField(max_length=30), blank=True, default=list, null=True)

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
