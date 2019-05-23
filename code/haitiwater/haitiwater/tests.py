from datetime import date

from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client

from apps.consumers.models import Consumer
from apps.financial.models import Invoice
from apps.water_network.models import Element, ElementType, ElementStatus, Zone


class GeneralTests(TestCase):
    fixtures = ["initial_data"]

    def setUp(self):
        self.client = Client()
        self.client.login(username="Protos", password="Protos")

    def tearDown(self):
        self.client.logout()

    def test_view_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_view_login(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_sw(self):
        response = self.client.get("/sw.js")
        self.assertEqual(response.status_code, 200)

    def test_register_cron(self):
        try:
            call_command("register_cron")
        except:
            self.fail("Should not crash")

    def test_run_cron_job(self):
        zone = Zone.objects.get(name="Haiti")

        fountain = Element(name="fountain", location="fountain", zone=zone,
                           type=ElementType.FOUNTAIN.name, status=ElementStatus.OK.name)
        indiv = Element(name="indiv", location="indiv", zone=zone,
                        type=ElementType.INDIVIDUAL.name, status=ElementStatus.OK.name)
        fountain.save()
        indiv.save()

        consumer_fountain = Consumer(first_name="test", last_name="test", water_outlet=fountain,
                                     gender="M", location="fountain", household_size=0)
        consumer_indiv = Consumer(first_name="test", last_name="test", water_outlet=indiv,
                                  gender="M", location="indiv", household_size=0)
        consumer_fountain.save()
        consumer_indiv.save()

        a_month_ago = date.today() + relativedelta(months=-1)
        invoice_old = Invoice(consumer=consumer_fountain, water_outlet=fountain,
                              amount=100, expiration=a_month_ago)
        invoice_old.save()

        invoice_fountain = Invoice(consumer=consumer_fountain, water_outlet=fountain,
                                   amount=100, expiration=date.today())
        invoice_indiv = Invoice(consumer=consumer_indiv, water_outlet=indiv,
                                amount=100, expiration=date.today())
        invoice_fountain.save()
        invoice_indiv.save()

        invoices = Invoice.objects.filter(expiration__gt=date.today())
        self.assertEqual(len(invoices), 0)

        call_command("cron")

        invoices = Invoice.objects.filter(expiration__gt=date.today())
        self.assertEqual(len(invoices), 1)
