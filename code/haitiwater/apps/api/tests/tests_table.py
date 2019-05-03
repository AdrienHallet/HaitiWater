import json

from django.contrib.auth.models import User, Group
from django.core.files import File
from django.db import connection
from django.test import TestCase, override_settings
from django.test.client import Client

from ...consumers.models import Consumer
from ...financial.models import Payment
from ...report.models import Ticket, BreakType, UrgencyType
from ...water_network.models import Zone, Element, ElementType, ElementStatus


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class TableTests(TestCase):
    fixtures = ["initial_data"]

    @classmethod  # Horrible hack to get the views
    def setUpClass(cls):
        super(TableTests, cls).setUpClass()

        file_handle = open('views.sql', 'r+')
        sql_file = File(file_handle)
        sql = sql_file.read()

        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()

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

        ticket = Ticket(water_outlet=fountain, type=BreakType.MECHANICAL.name,
                        comment="test", urgency=UrgencyType.LOW.name)
        ticket.save()

        payment = Payment(consumer=consumer_fountain, water_outlet=fountain, amount=100)
        payment.save()

        self.client.post("/api/gis/?id={}&action=add".format(fountain.id), {
            "geometry": {
                "type": "Point",
                "coordinates": [-72.331783, 19.394068]
            }
        }, content_type="application/json")

    def tearDown(self):
        self.client.logout()

    def test_get_table_not_connected(self):
        self.client.logout()

        response = self.client.get("/api/table/")
        self.assertEqual(response.status_code, 403)

    # Zone

    def test_get_zone(self):
        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 2)
        self.assertEqual(result["recordsFiltered"], 2)
        self.assertEqual(len(result["data"]), 2)

    def test_get_zone_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    def test_get_zone_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 403)

    # Element

    def test_get_element(self):
        response = self.client.get("/api/table/", {
            "name": "water_element",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 2)
        self.assertEqual(result["recordsFiltered"], 2)
        self.assertEqual(len(result["data"]), 2)

    def test_get_element_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/table/", {
            "name": "water_element",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_get_element_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/table/", {
            "name": "water_element",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    # Consumer

    def test_get_consumer(self):
        response = self.client.get("/api/table/", {
            "name": "consumer",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 2)
        self.assertEqual(result["recordsFiltered"], 2)
        self.assertEqual(len(result["data"]), 2)

    def test_get_consumer_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/table/", {
            "name": "consumer",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_get_consumer_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/table/", {
            "name": "consumer",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    # Manager

    def test_get_manager(self):
        response = self.client.get("/api/table/", {
            "name": "manager",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 3)
        self.assertEqual(result["recordsFiltered"], 3)
        self.assertEqual(len(result["data"]), 3)

    def test_get_manager_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/table/", {
            "name": "manager",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    def test_get_manager_unauthorized(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/table/", {
            "name": "manager",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 403)

    # Ticket

    def test_get_ticket(self):
        response = self.client.get("/api/table/", {
            "name": "ticket",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    def test_get_ticket_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/table/", {
            "name": "ticket",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_get_ticket_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/table/", {
            "name": "ticket",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    # Payment

    def test_get_payment(self):
        response = self.client.get("/api/table/", {
            "name": "payment",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

    def test_get_payment_user(self):
        consumer = Consumer.objects.get(last_name="fountain")
        response = self.client.get("/api/table/", {
            "name": "payment",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "user": consumer.id
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    def test_get_payment_sub(self):
        self.client.login(username="user_zone", password="test")

        consumer = Consumer.objects.get(last_name="fountain")
        response = self.client.get("/api/table/", {
            "name": "payment",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "user": consumer.id
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_get_payment_fountain(self):
        self.client.login(username="user_fountain", password="test")

        consumer = Consumer.objects.get(last_name="fountain")
        response = self.client.get("/api/table/", {
            "name": "payment",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "user": consumer.id
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 1)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    # Logs

    def test_get_log(self):
        response = self.client.get("/api/table/", {
            "name": "logs",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_get_log_history(self):
        response = self.client.get("/api/table/", {
            "name": "logs_history",
            "order[0][column]": "0",
            "order[0][dir]": "asc"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 0)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    # Datatable

    def test_search_none(self):
        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "search[value]": "test",
            "columns[1][searchable]": True
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 2)
        self.assertEqual(result["recordsFiltered"], 0)
        self.assertEqual(len(result["data"]), 0)

    def test_search_in(self):
        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "search[value]": "Haiti",
            "columns[1][searchable]": True
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 2)
        self.assertEqual(result["recordsFiltered"], 1)
        self.assertEqual(len(result["data"]), 1)

    def test_too_long(self):
        for i in range(18):
            self.client.post("/api/add/", {"table": "zone", "name": "test" + str(i)})

        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "start": "0",
            "length": "10"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 20)
        self.assertEqual(result["recordsFiltered"], 20)
        self.assertEqual(len(result["data"]), 10)

    def test_second_page(self):
        for i in range(18):
            self.client.post("/api/add/", {"table": "zone", "name": "test" + str(i)})

        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "asc",
            "start": "5",
            "length": "5"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 20)
        self.assertEqual(result["recordsFiltered"], 20)
        self.assertEqual(len(result["data"]), 5)

    def test_desc(self):
        for i in range(18):
            self.client.post("/api/add/", {"table": "zone", "name": "test" + str(i)})

        response = self.client.get("/api/table/", {
            "name": "zone",
            "order[0][column]": "0",
            "order[0][dir]": "desc",
            "start": "0",
            "length": "10"
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["recordsTotal"], 20)
        self.assertEqual(result["recordsFiltered"], 20)
        self.assertEqual(len(result["data"]), 10)

    # Graph

    def test_get_graph_not_connected(self):
        self.client.logout()

        response = self.client.get("/api/graph/")
        self.assertEqual(response.status_code, 403)

    def test_get_graph_gender(self):
        response = self.client.get("/api/graph/", {"type": "consumer_gender_pie"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"]), 3)
        self.assertEqual(result["jsonarray"][1]["data"], 2)

    def test_get_graph_gender_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/graph/", {"type": "consumer_gender_pie"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"]), 3)
        self.assertEqual(result["jsonarray"][1]["data"], 0)

    def test_get_graph_gender_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/graph/", {"type": "consumer_gender_pie"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"]), 3)
        self.assertEqual(result["jsonarray"][1]["data"], 1)

    def test_get_graph_volume(self):
        response = self.client.get("/api/graph/", {"type": "average_monthly_volume_per_zone"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"][0]["label"]), 2)

    def test_get_graph_volume_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/graph/", {"type": "average_monthly_volume_per_zone"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"][0]["label"]), 1)

    def test_get_graph_volume_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/graph/", {"type": "average_monthly_volume_per_zone"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["jsonarray"][0]["label"]), 1)

    # GIS

    def test_get_gis_not_connected(self):
        self.client.logout()

        response = self.client.get("/api/gis/")
        self.assertEqual(response.status_code, 403)

    def test_get_gis(self):
        response = self.client.get("/api/gis/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result), 1)

    def test_get_gis_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/gis/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result), 0)

    def test_get_gis_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/gis/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result), 1)

    def test_get_gis_marker(self):
        response = self.client.get("/api/gis/", {"marker": "fountain"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result), 1)

    def test_get_gis_no_marker(self):
        response = self.client.get("/api/gis/", {"marker": "kiosk"})
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result), 0)

    # Details

    def test_get_details_not_connected(self):
        self.client.logout()

        response = self.client.get("/api/details/")
        self.assertEqual(response.status_code, 403)

    def test_get_details_payment(self):
        consumer = Consumer.objects.get(last_name="fountain")
        response = self.client.get("/api/details/", {
            "table": "payment",
            "id": consumer.id
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["amount_due"], -100)

    def test_get_details_payment_not_exists(self):
        response = self.client.get("/api/details/", {
            "table": "payment",
            "id": 1000
        })
        self.assertEqual(response.status_code, 400)

    def test_get_details_payment_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        consumer = Consumer.objects.get(last_name="fountain")
        response = self.client.get("/api/details/", {
            "table": "payment",
            "id": consumer.id
        })
        self.assertEqual(response.status_code, 403)

    def test_get_details_location(self):
        fountain = Element.objects.get(name="fountain")
        response = self.client.get("/api/details/", {
            "table": "water_element",
            "id": fountain.id
        })
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(result["localization"], "fountain")
        self.assertIsNotNone(result["geoJSON"])

    def test_get_details_location_not_exists(self):
        response = self.client.get("/api/details/", {
            "table": "water_element",
            "id": 1000
        })
        self.assertEqual(response.status_code, 400)

    def test_get_details_location_unauthorized(self):
        self.client.login(username="user_zone", password="test")

        fountain = Element.objects.get(name="fountain")
        response = self.client.get("/api/details/", {
            "table": "water_element",
            "id": fountain.id
        })
        self.assertEqual(response.status_code, 403)

    # Outlets

    def test_get_outlets_not_connected(self):
        self.client.logout()

        response = self.client.get("/api/outlets/")
        self.assertEqual(response.status_code, 403)

    def test_get_outlets(self):
        response = self.client.get("/api/outlets/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["data"]), 2)

    def test_get_outlets_sub(self):
        self.client.login(username="user_zone", password="test")

        response = self.client.get("/api/outlets/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["data"]), 0)

    def test_get_outlets_fountain(self):
        self.client.login(username="user_fountain", password="test")

        response = self.client.get("/api/outlets/")
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEqual(len(result["data"]), 1)
