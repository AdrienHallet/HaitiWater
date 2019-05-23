from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from ...models import Invoice
from ....water_network.models import ElementType


class Command(BaseCommand):

    def handle(self, *args, **options):
        invoices = Invoice.objects.filter(expiration=date.today())\
            .exclude(water_outlet__type=ElementType.INDIVIDUAL.name)

        for invoice in invoices:
            consumer = invoice.consumer
            outlet = consumer.water_outlet
            price, duration = outlet.get_price_and_duration()
            creation = date.today()
            expiration = creation + relativedelta(months=duration)
            new_invoice = Invoice(consumer=consumer, water_outlet=outlet,
                                  creation=creation, expiration=expiration, amount=price)
            new_invoice.save()
