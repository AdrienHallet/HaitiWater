from django.contrib.auth.models import User, Group
from django.core.files import File
from django.db import connection
from django.test import TestCase
from django.test.client import Client

from ..water_network.models import Element, ElementStatus, ElementType, Zone


class LogTests(TestCase):
    fixtures = ["initial_data"]

    def setUp(self):
        self.client = Client()
        self.client.login(username="Protos", password="Protos")

        superzone = Zone.objects.get(name="Haiti")
        zone = Zone(name="zone", superzone=superzone, subzones=["zone"],
                    fountain_price=100, fountain_duration=10,
                    kiosk_price=200, kiosk_duration=12,
                    indiv_base_price=300)
        zone.save()

        superzone.subzones.append(zone.name)
        superzone.save()

        fountain = Element(name="fountain", type=ElementType.FOUNTAIN.name,
                           status=ElementStatus.OK.name, location="fountain", zone=superzone)
        fountain.save()

        user = User.objects.create_user(username="user_zone", email="test@gmail.com", password="test",
                                        first_name="test", last_name="test")
        user.profile.phone_number = None
        user.profile.zone = zone
        user.profile.save()
        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(user)

        user = User.objects.create_user(username="user_fountain", email="test@gmail.com", password="test",
                                        first_name="test", last_name="test")
        user.profile.phone_number = None
        user.profile.outlets.append(fountain.id)
        user.profile.save()
        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        my_group.user_set.add(user)

    def tearDown(self):
        self.client.logout()

    def test_view_log(self):
        response = self.client.get("/historique/")
        self.assertEqual(response.status_code, 200)

    def test_view_log_not_connected(self):
        self.client.logout()

        response = self.client.get("/historique/")
        self.assertEqual(response.status_code, 302)

    def test_view_log_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/historique/")
        self.assertEqual(response.status_code, 200)

    def test_view_log_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/historique/")
        self.assertEqual(response.status_code, 200)
