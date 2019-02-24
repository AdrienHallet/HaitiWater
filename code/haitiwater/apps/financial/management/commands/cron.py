import os
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from ...models import Invoice
from ....water_network.models import ElementType


class Command(BaseCommand):

    def handle(self, *args, **options):
        for invoice in Invoice.objects.filter(expiration=date.today()):
            if invoice.water_outlet.type != ElementType.INDIVIDUAL:
                consumer = invoice.consumer
                outlet = consumer.water_outlet
                creation = date.today()
                expiration = creation + timedelta(days=30*outlet.validity)
                amount = outlet.price
                new_invoice = Invoice(consumer=consumer, water_outlet=outlet,
                                      creation=creation, expiration=expiration, amount=amount)
                new_invoice.save()
