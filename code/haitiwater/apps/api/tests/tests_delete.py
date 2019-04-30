from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import User, Group
from apps.water_network.models import Zone, Location, Element, ElementType, ElementStatus
from apps.consumers.models import Consumer
from apps.report.models import Report, Ticket, BreakType, StatusType, UrgencyType
from apps.financial.models import Payment, Invoice


class DeleteTests(TestCase):
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

        lone_zone = Zone(name="lone", superzone=superzone, subzones=["lone"],
                         fountain_price=100, fountain_duration=10,
                         kiosk_price=200, kiosk_duration=12,
                         indiv_base_price=300)
        lone_zone.save()

        superzone.subzones.append(lone_zone.name)
        superzone.save()

        fountain = Element(name="fountain", type=ElementType.FOUNTAIN.name,
                           status=ElementStatus.OK.name, location="fountain", zone=superzone)
        fountain.save()

        indiv = Element(name="indiv", type=ElementType.INDIVIDUAL.name,
                        status=ElementStatus.OK.name, location="indiv", zone=superzone)
        indiv.save()

        lone_elem = Element(name="lone", type=ElementType.KIOSK.name,
                            status=ElementStatus.OK.name, location="lone", zone=superzone)
        lone_elem.save()

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
        user.profile.outlets.append(indiv.id)
        user.profile.save()
        my_group = Group.objects.get(name='Gestionnaire de fontaine')
        my_group.user_set.add(user)

        lone_user = User.objects.create_user(username="lone", email="test@gmail.com", password="test",
                                             first_name="test", last_name="test")
        lone_user.profile.phone_number = None
        lone_user.profile.zone = superzone
        lone_user.profile.save()
        my_group = Group.objects.get(name='Gestionnaire de zone')
        my_group.user_set.add(lone_user)

        lone_consumer = Consumer(first_name="consumer", last_name="fountain", gender="M",
                                 location="test", household_size=1, water_outlet=fountain)
        lone_consumer.save()

        lone_ticket = Ticket(water_outlet=fountain, type=BreakType.MECHANICAL.name,
                             comment="test", urgency=UrgencyType.LOW.name)
        lone_ticket.save()

        lone_payment = Payment(consumer=lone_consumer, water_outlet=fountain, amount=100)
        lone_payment.save()

        self.client.post("/api/gis/?id={}&action=add".format(fountain.id), {
            "geometry": {
                "type": "Point",
                "coordinates": [-72.331783, 19.394068]
            }
        }, content_type="application/json")

    def tearDown(self):
        self.client.logout()

    # Zone

    def test_delete_zone(self):
        old_zone = Zone.objects.get(name="lone")
        response = self.client.post("/api/remove/", {
            "table": "zone",
            "id": old_zone.id
        })
        self.assertEqual(response.status_code, 200)

        test_zone = Zone.objects.filter(name="lone").first()
        self.assertIsNone(test_zone)

        superzone = Zone.objects.get(name="Haiti")
        self.assertNotIn(old_zone.name, superzone.subzones)

    def test_delete_zone_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        old_zone = Zone.objects.get(name="lone")
        response = self.client.post("/api/remove/", {
            "table": "zone",
            "id": old_zone.id
        })
        self.assertEqual(response.status_code, 403)

        test_zone = Zone.objects.filter(name="lone").first()
        self.assertIsNotNone(test_zone)

    def test_delete_zone_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "zone",
            "id": 100
        })
        self.assertEqual(response.status_code, 400)

        test_zone = Zone.objects.filter(id=100).first()
        self.assertIsNone(test_zone)

    def test_delete_zone_used(self):
        old_zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/remove/", {
            "table": "zone",
            "id": old_zone.id
        })
        self.assertEqual(response.status_code, 400)

        test_zone = Zone.objects.filter(name="zone").first()
        self.assertIsNotNone(test_zone)

    # Element

    def test_delete_elem(self):
        old_elem = Element.objects.get(name="lone")
        response = self.client.post("/api/remove/", {
            "table": "water_element",
            "id": old_elem.id
        })
        self.assertEqual(response.status_code, 200)

        test_elem = Element.objects.filter(name="lone").first()
        self.assertIsNone(test_elem)

    def test_delete_elem_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "water_element",
            "id": 100
        })
        self.assertEqual(response.status_code, 400)

        test_elem = Element.objects.filter(id=100).first()
        self.assertIsNone(test_elem)

    def test_delete_elem_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_elem = Element.objects.get(name="lone")
        response = self.client.post("/api/remove/", {
            "table": "water_element",
            "id": old_elem.id
        })
        self.assertEqual(response.status_code, 403)

        test_elem = Element.objects.filter(name="lone").first()
        self.assertIsNotNone(test_elem)

    def test_delete_elem_used(self):
        old_elem = Element.objects.get(name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "water_element",
            "id": old_elem.id
        })
        self.assertEqual(response.status_code, 400)

        test_elem = Element.objects.filter(name="fountain").first()
        self.assertIsNotNone(test_elem)

    def test_delete_elem_with_user(self):
        old_elem = Element.objects.get(name="indiv")

        user = User.objects.get(username="user_fountain")
        self.assertIn(str(old_elem.id), user.profile.outlets)

        response = self.client.post("/api/remove/", {
            "table": "water_element",
            "id": old_elem.id
        })
        self.assertEqual(response.status_code, 200)

        test_elem = Element.objects.filter(name="indiv").first()
        self.assertIsNone(test_elem)

        user = User.objects.get(username="user_fountain")
        self.assertNotIn(str(old_elem.id), user.profile.outlets)

    # Consumer

    def test_delete_consumer(self):
        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "consumer",
            "id": old_consumer.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNone(test_consumer)

    def test_delete_consumer_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "consumer",
            "id": 100
        })
        self.assertEqual(response.status_code, 400)

        test_consumer = Consumer.objects.filter(id=100).first()
        self.assertIsNone(test_consumer)

    def test_delete_consumer_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "consumer",
            "id": old_consumer.id
        })
        self.assertEqual(response.status_code, 403)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNotNone(test_consumer)

    # User

    def test_delete_user(self):
        old_user = User.objects.get(username="lone")
        response = self.client.post("/api/remove/", {
            "table": "manager",
            "id": old_user.username
        })
        self.assertEqual(response.status_code, 200)

        test_user = User.objects.filter(username="lone").first()
        self.assertIsNone(test_user)

    def test_delete_user_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        old_user = User.objects.get(username="lone")
        response = self.client.post("/api/remove/", {
            "table": "manager",
            "id": old_user.username
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="lone").first()
        self.assertIsNotNone(test_user)

    def test_delete_user_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "manager",
            "id": "not_exist"
        })
        self.assertEqual(response.status_code, 400)

        test_user = User.objects.filter(username="not_exist").first()
        self.assertIsNone(test_user)

    def test_delete_user_higher(self):
        self.client.login(username="user_zone", password="test")

        old_user = User.objects.get(username="lone")
        response = self.client.post("/api/remove/", {
            "table": "manager",
            "id": old_user.username
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="lone").first()
        self.assertIsNotNone(test_user)

    # Ticket

    def test_delete_ticket(self):
        old_ticket = Ticket.objects.get(water_outlet__name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "ticket",
            "id": old_ticket.id
        })
        self.assertEqual(response.status_code, 200)

        test_ticket = Ticket.objects.filter(water_outlet__name="fountain").first()
        self.assertIsNone(test_ticket)

    def test_delete_ticket_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "ticket",
            "id": 100
        })
        self.assertEqual(response.status_code, 400)

        test_ticket = Ticket.objects.filter(id=100).first()
        self.assertIsNone(test_ticket)

    def test_delete_ticket_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_ticket = Ticket.objects.get(water_outlet__name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "ticket",
            "id": old_ticket.id
        })
        self.assertEqual(response.status_code, 403)

        test_ticket = Ticket.objects.filter(water_outlet__name="fountain").first()
        self.assertIsNotNone(test_ticket)

    # Payment

    def test_delete_payment(self):
        old_payment = Payment.objects.get(water_outlet__name="fountain", consumer__last_name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "payment",
            "id": old_payment.id
        })
        self.assertEqual(response.status_code, 200)

        test_payment = Payment.objects.filter(water_outlet__name="fountain", consumer__last_name="fountain").first()
        self.assertIsNone(test_payment)

    def test_delete_payment_not_exists(self):
        response = self.client.post("/api/remove/", {
            "table": "payment",
            "id": 100
        })
        self.assertEqual(response.status_code, 400)

        test_payment = Payment.objects.filter(id=100).first()
        self.assertIsNone(test_payment)

    def test_delete_payment_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_payment = Payment.objects.get(water_outlet__name="fountain", consumer__last_name="fountain")
        response = self.client.post("/api/remove/", {
            "table": "payment",
            "id": old_payment.id
        })
        self.assertEqual(response.status_code, 403)

        test_payment = Payment.objects.filter(water_outlet__name="fountain", consumer__last_name="fountain").first()
        self.assertIsNotNone(test_payment)

    # Location

    def test_delete_location(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/gis/?id={}&action=remove".format(fountain.id))
        self.assertEqual(response.status_code, 200)

        test_location = Location.objects.filter(elem__name="fountain").first()
        self.assertIsNone(test_location)

    def test_delete_location_not_exists(self):
        response = self.client.post("/api/gis/?id=100&action=remove")
        self.assertEqual(response.status_code, 400)

        test_location = Location.objects.filter(elem__id=100).first()
        self.assertIsNone(test_location)

    def test_delete_location_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/gis/?id={}&action=remove".format(fountain.id))
        self.assertEqual(response.status_code, 403)

        test_location = Location.objects.filter(elem__name="fountain").first()
        self.assertIsNotNone(test_location)
