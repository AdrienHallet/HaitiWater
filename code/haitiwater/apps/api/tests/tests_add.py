from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test.client import Client

from ...consumers.models import Consumer
from ...financial.models import Payment, Invoice
from ...report.models import Report, Ticket, BreakType, UrgencyType
from ...water_network.models import Zone, Location, Element, ElementType, ElementStatus


class AddTests(TestCase):
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
                        status=ElementStatus.OK.name, location="indiv", zone=superzone)
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

    def tearDown(self):
        self.client.logout()

    # Add Zone

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

    def test_add_zone_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.post("/api/add/", {
            "table": "zone",
            "name": "TestZone",
            "fountain-price": 100,
            "fountain-duration": 10,
            "kiosk-price": 200,
            "kiosk-duration": 12,
            "indiv-price": 300
        })
        self.assertEqual(response.status_code, 403)

        test_zone = Zone.objects.filter(name="TestZone").first()
        self.assertIsNone(test_zone)

    def test_add_zone_twice(self):
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

        response = self.client.post("/api/add/", {
            "table": "zone",
            "name": "TestZone",
            "fountain-price": 100,
            "fountain-duration": 10,
            "kiosk-price": 200,
            "kiosk-duration": 12,
            "indiv-price": 300
        })
        self.assertEqual(response.status_code, 400)

        test_zone = Zone.objects.filter(name="TestZone")
        self.assertEqual(len(test_zone), 1)

    def test_add_more_zones(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.post("/api/add/", {
            "table": "zone",
            "name": "TestSubZone",
            "fountain-price": 100,
            "fountain-duration": 10,
            "kiosk-price": 200,
            "kiosk-duration": 12,
            "indiv-price": 300
        })
        self.assertEqual(response.status_code, 200)

        supersuperzone = Zone.objects.get(name="Haiti")
        self.assertIn("TestSubZone", supersuperzone.subzones)

        superzone = Zone.objects.get(name="zone")
        self.assertIn("TestSubZone", superzone.subzones)

        test_zone = Zone.objects.filter(name="TestSubZone").first()
        self.assertIsNotNone(test_zone)
        self.assertEqual(test_zone.superzone, superzone)

    # Add element

    def test_add_element(self):
        response = self.client.post("/api/add/", {
            "table": "water_element",
            "type": "fountain",
            "localization": "test",
            "state": "ok"
        })
        self.assertEqual(response.status_code, 200)

        test_element = Element.objects.filter(location="test").first()
        self.assertIsNotNone(test_element)

    def test_add_element_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.post("/api/add/", {
            "table": "water_element",
            "type": "fountain",
            "localization": "test",
            "state": "ok"
        })
        self.assertEqual(response.status_code, 403)

        test_element = Element.objects.filter(location="test").first()
        self.assertIsNone(test_element)

    # Add consumer

    def test_add_consumer(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": fountain.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNotNone(test_consumer)

        test_invoice = Invoice.objects.filter(consumer=test_consumer).first()
        self.assertIsNotNone(test_invoice)

    def test_add_consumer_indiv(self):
        indiv = Element.objects.get(name="indiv")
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": indiv.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNotNone(test_consumer)

        test_invoice = Invoice.objects.filter(consumer=test_consumer).first()
        self.assertIsNone(test_invoice)

    def test_add_consumer_no_fountain(self):
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": 100
        })
        self.assertEqual(response.status_code, 400)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNone(test_consumer)

    def test_add_consumer_no_int(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": "none",
            "phone": "",
            "mainOutlet": fountain.id
        })
        self.assertEqual(response.status_code, 400)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNone(test_consumer)

    def test_add_consumer_no_access(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": fountain.id
        })
        self.assertEqual(response.status_code, 403)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNone(test_consumer)

    def test_add_consumer_user_fountain(self):
        self.client.login(username="user_fountain", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "consumer",
            "firstname": "test",
            "lastname": "test",
            "gender": "M",
            "address": "test",
            "subconsumer": 0,
            "phone": "",
            "mainOutlet": fountain.id
        })
        self.assertEqual(response.status_code, 200)

        test_consumer = Consumer.objects.filter(first_name="test", last_name="test").first()
        self.assertIsNotNone(test_consumer)

        test_invoice = Invoice.objects.filter(consumer=test_consumer).first()
        self.assertIsNotNone(test_invoice)

    # Report

    def test_add_report(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/report/", {
            "selectedOutlets": [fountain.id],
            "isActive": True,
            "inputHours": 12,
            "inputDays": 20,
            "details": [
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        test_report_line = Report.objects.filter(water_outlet=fountain).first()
        self.assertIsNotNone(test_report_line)

        consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        invoice = Invoice.objects.filter(consumer=consumer).first()
        self.assertIsNone(invoice)

    def test_add_report_indiv(self):
        indiv = Element.objects.get(name="indiv")
        response = self.client.post("/api/report/", {
            "selectedOutlets": [indiv.id],
            "isActive": True,
            "inputHours": 12,
            "inputDays": 20,
            "details": [
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        test_report_line = Report.objects.filter(water_outlet=indiv).first()
        self.assertIsNotNone(test_report_line)

        consumer = Consumer.objects.get(first_name="consumer", last_name="indiv")
        invoice = Invoice.objects.filter(consumer=consumer).first()
        self.assertIsNotNone(invoice)

    def test_add_report_multiple_outlet(self):
        fountain = Element.objects.get(name="fountain")
        indiv = Element.objects.get(name="indiv")
        response = self.client.post("/api/report/", {
            "selectedOutlets": [fountain.id, indiv.id],
            "isActive": True,
            "inputHours": 12,
            "inputDays": 20,
            "details": [
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                },
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        test_report_line_fountain = Report.objects.filter(water_outlet=fountain).first()
        self.assertIsNotNone(test_report_line_fountain)

        test_report_line_indiv = Report.objects.filter(water_outlet=indiv).first()
        self.assertIsNotNone(test_report_line_indiv)

    def test_add_report_no_fountain(self):
        response = self.client.post("/api/report/", {
            "selectedOutlets": [100],
            "isActive": True,
            "inputHours": 12,
            "inputDays": 20,
            "details": [
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        test_report_line = Report.objects.filter(water_outlet__id=100).first()
        self.assertIsNone(test_report_line)

    def test_add_report_no_access(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/report/", {
            "selectedOutlets": [fountain.id],
            "isActive": True,
            "inputHours": 12,
            "inputDays": 20,
            "details": [
                {
                    "perCubic": 100,
                    "cubic": 100,
                    "bill": 10000
                }
            ]
        }, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        test_report = Report.objects.filter(water_outlet=fountain).first()
        self.assertIsNone(test_report)

    # User

    def test_add_user_zone(self):
        zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 200)

        test_user = User.objects.filter(username="user_test").first()
        self.assertIsNotNone(test_user)

    def test_add_user_fountain(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "fountain-manager",
            "outlets": fountain.id
        })
        self.assertEqual(response.status_code, 200)

        test_user = User.objects.filter(username="user_test").first()
        self.assertIsNotNone(test_user)

        self.assertIn(test_user.first_name + " " + test_user.last_name, fountain.get_managers())

    def test_add_user_twice(self):
        zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 400)

        test_user = User.objects.filter(username="user_test")
        self.assertEqual(len(test_user), 1)

    def test_add_user_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        zone = Zone.objects.get(name="zone")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="user_test").first()
        self.assertIsNone(test_user)

    def test_add_user_zone_higher(self):
        self.client.login(username="user_zone", password="test")

        zone = Zone.objects.get(name="Haiti")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "zone-manager",
            "zone": zone.id
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="user_test").first()
        self.assertIsNone(test_user)

    def test_add_user_fountain_higher(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "manager",
            "firstname": "test",
            "lastname": "test",
            "id": "user_test",
            "email": "test@gmail.com",
            "phone": "",
            "type": "fountain-manager",
            "outlets": fountain.id
        })
        self.assertEqual(response.status_code, 403)

        test_user = User.objects.filter(username="user_test").first()
        self.assertIsNone(test_user)

    # Ticket

    def test_add_ticket(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "ticket",
            "id_outlet": fountain.id,
            "type": BreakType.MECHANICAL.name,
            "comment": "test",
            "urgency": UrgencyType.LOW.name
        })
        self.assertEqual(response.status_code, 200)

        test_ticket = Ticket.objects.filter(comment="test").first()
        self.assertIsNotNone(test_ticket)

    def test_add_ticket_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/add/", {
            "table": "ticket",
            "id_outlet": fountain.id,
            "type": BreakType.MECHANICAL.name,
            "comment": "test",
            "urgency": UrgencyType.LOW.name
        })
        self.assertEqual(response.status_code, 403)

        test_ticket = Ticket.objects.filter(comment="test").first()
        self.assertIsNone(test_ticket)

    # Payment

    def test_add_payment(self):
        consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/add/", {
            "table": "payment",
            "id_consumer": consumer.id,
            "amount": 100
        })
        self.assertEqual(response.status_code, 200)

        test_payment = Payment.objects.filter(consumer=consumer).first()
        self.assertIsNotNone(test_payment)

    def test_add_payment_no_consumer(self):
        response = self.client.post("/api/add/", {
            "table": "payment",
            "id_consumer": 100,
            "amount": 100
        })
        self.assertEqual(response.status_code, 400)

        test_payment = Payment.objects.filter(consumer__id=100).first()
        self.assertIsNone(test_payment)

    def test_add_payment_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        consumer = Consumer.objects.get(first_name="consumer", last_name="fountain")
        response = self.client.post("/api/add/", {
            "table": "payment",
            "id_consumer": consumer.id,
            "amount": 100
        })
        self.assertEqual(response.status_code, 403)

        test_payment = Payment.objects.filter(consumer=consumer).first()
        self.assertIsNone(test_payment)

    # Location

    def test_add_location(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/gis/?id={}&action=add".format(fountain.id), {
            "geometry": {
                "type": "Point",
                "coordinates": [-72.331783, 19.394068]
            }
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        test_location = Location.objects.filter(elem=fountain).first()
        self.assertIsNotNone(test_location)

    def test_add_location_no_elem(self):
        response = self.client.post("/api/gis/?id=100&action=add", {
            "geometry": {
                "type": "Point",
                "coordinates": [-72.331783, 19.394068]
            }
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        test_location = Location.objects.filter(elem__id=100).first()
        self.assertIsNone(test_location)

    def test_add_location_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.post("/api/gis/?id={}&action=add".format(fountain.id), {
            "geometry": {
                "type": "Point",
                "coordinates": [-72.331783, 19.394068]
            }
        }, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        test_location = Location.objects.filter(elem=fountain).first()
        self.assertIsNone(test_location)