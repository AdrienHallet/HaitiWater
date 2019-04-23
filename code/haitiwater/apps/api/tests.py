from django.test import TestCase
from django.test.client import Client

from ..water_network.models import Zone


class GeneralTests(TestCase):
    fixtures = ["initial_data"]

    def setUp(self):
        self.client = Client()

    def test_fixture(self):
        zone = Zone.objects.filter(name="Haiti").first()
        self.assertIsNotNone(zone)

    def test_connect(self):
        response = self.client.get("/api/graph/", {"type": "consumer_gender_pie"})
        self.assertEqual(response.status_code, 403)

        connected = self.client.login(username="Protos", password="Protos")
        self.assertTrue(connected)

        response = self.client.get("/api/graph/", {"type": "consumer_gender_pie"})
        self.assertEqual(response.status_code, 200)

        self.client.logout()


class AddTests(TestCase):
    fixtures = ["initial_data"]

    def setUp(self):
        self.client = Client()
        self.client.login(username="Protos", password="Protos")

    def tearDown(self):
        self.client.logout()

    def test_add_zone(self):
        response = self.client.post("/api/add/", {
            "table": "zone",
            "name": "TestZone",
            "fountain-price": 100,
            "fountain-duration": 10,
            "kiosk-price": 200,
            "kiosk-duration": 12,
            "indiv-price": 300
        })
        self.assertEqual(response.status_code, 200)

        superzone = Zone.objects.get(name="Haiti")
        self.assertIn("TestZone", superzone.subzones)

        test_zone = Zone.objects.filter(name="TestZone").first()
        self.assertIsNotNone(test_zone)
        self.assertEqual(test_zone.superzone, superzone)
