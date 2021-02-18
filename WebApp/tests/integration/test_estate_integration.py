import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate


# Create your tests here.


class EstateIntegrationTest(TestCase):

    def setUp(self):
        self.user: get_user_model
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Solfrid 90", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)

    def test_endpoint(self):
        c = Client()
        response = c.get("/DB/")
        self.assertEqual(200, response.status_code)

    def test_show_estate(self):
        c = Client()
        response = c.get("/DB/")
        self.assertContains(response, "Solfrid 90")
