from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..water_network.models import Zone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, verbose_name="Zone gérée",
                             related_name="admins", on_delete=models.CASCADE)

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
