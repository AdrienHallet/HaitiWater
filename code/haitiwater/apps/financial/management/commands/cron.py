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
                price, duration = outlet.get_price_and_duration()
                creation = date.today()
                expiration = creation + timedelta(days=duration*30)  # TODO each month
                new_invoice = Invoice(consumer=consumer, water_outlet=outlet,
                                      creation=creation, expiration=expiration, amount=price)
                new_invoice.save()
