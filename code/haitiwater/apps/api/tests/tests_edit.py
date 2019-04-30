from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test.client import Client

from ...consumers.models import Consumer
from ...financial.models import Payment
from ...report.models import Ticket, BreakType, StatusType, UrgencyType
from ...water_network.models import Zone, Element, ElementType, ElementStatus


class EditTests(TestCase):
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

        indiv = Element(name="indiv", type=ElementType.INDIVIDUAL.name,
                        status=ElementStatus.OK, location="indiv", zone=superzone)
        indiv.save()

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

        consumer_fountain = Consumer(first_name="consumer", last_name="fountain", gender="M",
                                     location="test", household_size=1, water_outlet=fountain)
        consumer_fountain.save()

        consumer_indiv = Consumer(first_name="consumer", last_name="indiv", gender="M",
                                  location="test", household_size=1, water_outlet=indiv)
        consumer_indiv.save()

        ticket = Ticket(water_outlet=fountain, type=BreakType.MECHANICAL.name,
                        comment="test", urgency=UrgencyType.LOW.name)
        ticket.save()

        payment = Payment(consumer=consumer_fountain, water_outlet=fountain, amount=100)
        payment.save()

    def tearDown(self):
        self.client.logout()

    # Zone

    def test_edit_zone(self):
        old_zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/edit/", {
            "table": "zone",
            "id": old_zone.id,
            "name": "test",
            "fountain-price": old_zone.fountain_price,
            "fountain-duration": old_zone.fountain_duration,
            "kiosk-price": old_zone.kiosk_price,
            "kiosk-duration": old_zone.kiosk_duration,
            "indiv-price": old_zone.indiv_base_price
        })
        self.assertEqual(response.status_code, 200)

        test_zone = Zone.objects.filter(name="zone").first()
        self.assertIsNone(test_zone)

        test_zone = Zone.objects.filter(name="test").first()
        self.assertIsNotNone(test_zone)

        self.assertNotEqual(old_zone.name, test_zone.name)

        superzone = Zone.objects.get(name="Haiti")
        self.assertIn("test", superzone.subzones)
        self.assertNotIn("zone", superzone.subzones)

    def test_edit_zone_not_exists(self):
        response = self.client.post("/api/edit/", {
            "table": "zone",
            "id": 100,
            "name": "test",
            "fountain-price": 100,
            "fountain-duration": 10,
            "kiosk-price": 200,
            "kiosk-duration": 12,
            "indiv-price": 300
        })
        self.assertEqual(response.status_code, 400)

        test_zone = Zone.objects.filter(name="test").first()
        self.assertIsNone(test_zone)

    def test_edit_zone_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        old_zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/edit/", {
            "table": "zone",
            "id": old_zone.id,
            "name": "test",
            "fountain-price": old_zone.fountain_price,
            "fountain-duration": old_zone.fountain_duration,
            "kiosk-price": old_zone.kiosk_price,
            "kiosk-duration": old_zone.kiosk_duration,
            "indiv-price": old_zone.indiv_base_price
        })
        self.assertEqual(response.status_code, 403)

        test_zone = Zone.objects.filter(name="test").first()
        self.assertIsNone(test_zone)

        test_zone = Zone.objects.filter(name="zone").first()
        self.assertIsNotNone(test_zone)

    # Element

    def test_edit_element(self):
        old_element = Element.objects.get(name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "water_element",
            "id": old_element.id,
            "type": old_element.type,
            "localization": "test",
            "state": old_element.status
        })
        self.assertEqual(response.status_code, 200)

        test_element = Element.objects.filter(name="fountain").first()
        self.assertIsNone(test_element)

        test_element = Element.objects.filter(name__contains="test").first()
        self.assertIsNotNone(test_element)

        self.assertNotEqual(old_element.location, test_element.location)

    def test_edit_element_not_exists(self):
        response = self.client.post("/api/edit/", {
            "table": "water_element",
            "id": 100,
            "type": ElementType.FOUNTAIN.name,
            "localization": "test",
            "state": ElementStatus.OK.name
        })
        self.assertEqual(response.status_code, 400)

        test_element = Element.objects.filter(name__contains="test").first()
        self.assertIsNone(test_element)

    def test_edit_element_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_element = Element.objects.get(name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "water_element",
            "id": old_element.id,
            "type": old_element.type,
            "localization": "test",
            "state": old_element.status
        })
        self.assertEqual(response.status_code, 403)

        test_element = Element.objects.filter(name__contains="test").first()
        self.assertIsNone(test_element)

        test_element = Element.objects.filter(name="fountain").first()
        self.assertIsNotNone(test_element)

        self.assertEqual(old_element.location, test_element.location)

    def test_edit_element_type(self):
        old_element = Element.objects.get(name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "water_element",
            "id": old_element.id,
            "type": ElementType.INDIVIDUAL.name,
            "localization": old_element.location,
            "state": old_element.status
        })
        self.assertEqual(response.status_code, 200)

        test_element = Element.objects.filter(name="fountain").first()
        self.assertIsNone(test_element)

        test_element = Element.objects.filter(name__contains="fountain").first()
        self.assertIsNotNone(test_element)

        self.assertNotEqual(old_element.type, test_element.type)

    # Consumer

    def test_edit_consumer(self):
        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "consumer",
            "id": old_consumer.id,
            "firstname": old_consumer.first_name,
            "lastname": old_consumer.last_name,
            "gender": old_consumer.gender,
            "address": "new test",
            "subconsumer": old_consumer.household_size,
            "phone": old_consumer.phone_number,
            "mainOutlet": old_consumer.water_outlet.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNotNone(test_consumer)

        self.assertNotEqual(old_consumer.location, test_consumer.location)

    def test_edit_consumer_not_exists(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "consumer",
            "id": 100,
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": fountain.id
        })
        self.assertEqual(response.status_code, 400)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNone(test_consumer)

    def test_edit_consumer_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "consumer",
            "id": old_consumer.id,
            "firstname": old_consumer.first_name,
            "lastname": old_consumer.last_name,
            "gender": old_consumer.gender,
            "address": "new test",
            "subconsumer": old_consumer.household_size,
            "phone": old_consumer.phone_number,
            "mainOutlet": old_consumer.water_outlet.id
        })
        self.assertEqual(response.status_code, 403)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNotNone(test_consumer)

        self.assertEqual(old_consumer.location, test_consumer.location)

    def test_edit_consumer_name(self):
        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "consumer",
            "id": old_consumer.id,
            "firstname": "test",
            "lastname": "test",
            "gender": old_consumer.gender,
            "address": old_consumer.location,
            "subconsumer": old_consumer.household_size,
            "phone": old_consumer.phone_number,
            "mainOutlet": old_consumer.water_outlet.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNone(test_consumer)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNotNone(test_consumer)

        self.assertEqual(old_consumer.location, test_consumer.location)

    def test_edit_consumer_outlet(self):
        indiv = Element.objects.get(name="indiv")
        old_consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "consumer",
            "id": old_consumer.id,
            "firstname": old_consumer.first_name,
            "lastname": old_consumer.last_name,
            "gender": old_consumer.gender,
            "address": old_consumer.location,
            "subconsumer": old_consumer.household_size,
            "phone": old_consumer.phone_number,
            "mainOutlet": indiv.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="consumer", last_name="fountain").first()
        self.assertIsNotNone(test_consumer)

        self.assertNotEqual(old_consumer.water_outlet, test_consumer.water_outlet)

    # Ticket

    def test_edit_ticket(self):
        old_ticket = Ticket.objects.get(water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "ticket",
            "id": old_ticket.id,
            "id_outlet": old_ticket.water_outlet.id,
            "urgency": old_ticket.urgency,
            "type": old_ticket.type,
            "comment": "new test",
            "state": old_ticket.status
        })
        self.assertEqual(response.status_code, 200)

        test_ticket = Ticket.objects.filter(water_outlet__name="fountain").first()
        self.assertIsNotNone(test_ticket)

        self.assertNotEqual(old_ticket.comment, test_ticket.comment)

    def test_edit_ticket_not_exists(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "ticket",
            "id": 100,
            "id_outlet": fountain.id,
            "urgency": UrgencyType.LOW.name,
            "type": BreakType.MECHANICAL.name,
            "comment": "test",
            "state": StatusType.CURRENT.name
        })
        self.assertEqual(response.status_code, 400)

        test_ticket = Ticket.objects.filter(id=100).first()
        self.assertIsNone(test_ticket)

    def test_edit_ticket_not_authorized(self):
        self.client.login(username="user_zone", password="test")

        old_ticket = Ticket.objects.get(water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "ticket",
            "id": old_ticket.id,
            "id_outlet": old_ticket.water_outlet.id,
            "urgency": old_ticket.urgency,
            "type": old_ticket.type,
            "comment": "new test",
            "state": old_ticket.status
        })
        self.assertEqual(response.status_code, 403)

        test_ticket = Ticket.objects.filter(water_outlet__name="fountain").first()
        self.assertIsNotNone(test_ticket)

        self.assertEqual(old_ticket.comment, test_ticket.comment)

    def test_edit_ticket_outlet(self):
        indiv = Element.objects.get(name="indiv")
        old_ticket = Ticket.objects.get(water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "ticket",
            "id": old_ticket.id,
            "id_outlet": indiv.id,
            "urgency": old_ticket.urgency,
            "type": old_ticket.type,
            "comment": old_ticket.comment,
            "state": old_ticket.status
        })
        self.assertEqual(response.status_code, 200)

        test_ticket = Ticket.objects.filter(water_outlet__name="indiv").first()
        self.assertIsNotNone(test_ticket)

        self.assertNotEqual(old_ticket.water_outlet, test_ticket.water_outlet)

    # User

    def test_edit_user(self):
        old_user = User.objects.get(username="user_zone")
        response = self.client.post("/api/edit/", {
            "table": "manager",
            "id": old_user.username,
            "phone": "test",
            "type": "zone-manager",
            "zone": old_user.profile.zone.id
        })
        self.assertEqual(response.status_code, 200)

        test_user = User.objects.filter(username="user_zone").first()
        self.assertIsNotNone(test_user)

        self.assertNotEqual(old_user.profile.phone_number, test_user.profile.phone_number)

    def test_edit_user_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        old_user = User.objects.get(username="user_zone")
        response = self.client.post("/api/edit/", {
            "table": "manager",
            "id": old_user.username,
            "phone": "test",
            "type": "zone-manager",
            "zone": old_user.profile.zone.id
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="user_zone").first()
        self.assertIsNotNone(test_user)

        self.assertEqual(old_user.profile.phone_number, test_user.profile.phone_number)

    def test_edit_user_not_exists(self):
        zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/edit/", {
            "table": "manager",
            "id": "test",
            "phone": "test",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 400)

        test_user = User.objects.filter(username="test").first()
        self.assertIsNone(test_user)

    def test_edit_user_type(self):
        fountain = Element.objects.get(name="fountain")
        old_user = User.objects.get(username="user_zone")
        response = self.client.post("/api/edit/", {
            "table": "manager",
            "id": old_user.username,
            "phone": "test",
            "type": "fountain-manager",
            "outlets": fountain.id
        })
        self.assertEqual(response.status_code, 200)

        test_user = User.objects.filter(username="user_zone").first()
        self.assertIsNotNone(test_user)

        self.assertIsNone(test_user.profile.zone)
        self.assertIn(str(fountain.id), test_user.profile.outlets)

    # Payment

    def test_edit_payment(self):
        old_payment = Payment.objects.get(consumer__last_name="fountain", water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "payment",
            "id": old_payment.id,
            "id_consumer": old_payment.consumer.id,
            "amount": 200
        })
        self.assertEqual(response.status_code, 200)

        test_payment = Payment.objects.filter(consumer__last_name="fountain", water_outlet__name="fountain").first()
        self.assertIsNotNone(test_payment)

        self.assertNotEqual(old_payment.amount, test_payment.amount)

    def test_edit_payment_not_exists(self):
        consumer = Consumer.objects.get(first_name="consumer", last_name="indiv")
        response = self.client.post("/api/edit/", {
            "table": "payment",
            "id": 100,
            "id_consumer": consumer.id,
            "amount": 100
        })
        self.assertEqual(response.status_code, 400)

        test_payment = Payment.objects.filter(consumer__last_name="indiv", water_outlet__name="indiv").first()
        self.assertIsNone(test_payment)

    def test_edit_payment_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        old_payment = Payment.objects.get(consumer__last_name="fountain", water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "payment",
            "id": old_payment.id,
            "id_consumer": old_payment.consumer.id,
            "amount": 200
        })
        self.assertEqual(response.status_code, 403)

        test_payment = Payment.objects.filter(consumer__last_name="fountain", water_outlet__name="fountain").first()
        self.assertIsNotNone(test_payment)

        self.assertEqual(old_payment.amount, test_payment.amount)

    def test_edit_payment_consumer(self):
        consumer = Consumer.objects.get(first_name="consumer", last_name="indiv")
        old_payment = Payment.objects.get(consumer__last_name="fountain", water_outlet__name="fountain")
        response = self.client.post("/api/edit/", {
            "table": "payment",
            "id": old_payment.id,
            "id_consumer": consumer.id,
            "amount": old_payment.amount
        })

        self.assertEqual(response.status_code, 200)

        test_payment = Payment.objects.filter(consumer__last_name="fountain", water_outlet__name="fountain").first()
        self.assertIsNone(test_payment)

        test_payment = Payment.objects.filter(consumer__last_name="indiv", water_outlet__name="indiv").first()
        self.assertIsNotNone(test_payment)

        self.assertNotEqual(old_payment.consumer, test_payment.consumer)
