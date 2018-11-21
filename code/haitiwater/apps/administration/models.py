from django.db import models

from ..consumers.models import Person
from ..water_network.models import Zone, Element


class ZoneAdministrator(Person):

    zone = models.ForeignKey(Zone, verbose_name="Zone en charge", related_name="admin", on_delete=models.CASCADE)


class PointAdministrator(Person):

    point = models.ForeignKey(Element, verbose_name="Fontaine en charge", related_name="admin", on_delete=models.CASCADE)
