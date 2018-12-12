from django.db import models

from ..consumers.models import Person
from ..water_network.models import Zone
from django.contrib.auth.models import User


#class Authentication(Person):
    #authUser = models.OneToOneField(User, on_delete=models.CASCADE)
    #TODO permissions
    #zone = models.ForeignKey(Zone, verbose_name="Zone gérée",
    #                         related_name="admins", on_delete=models.CASCADE)
