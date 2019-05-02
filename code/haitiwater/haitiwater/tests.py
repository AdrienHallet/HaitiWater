from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client


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
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_run_cron_job(self):
        try:
            call_command("cron")
            self.assertTrue(True)
        except:
            self.assertTrue(False)
