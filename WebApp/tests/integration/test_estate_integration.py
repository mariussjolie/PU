"""Module containing Integration test for estate"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate


# Create your tests here.


class EstateIntegrationTest(TestCase):
    """Estate Integration Test"""

    def setUp(self):
        """Set up test objects"""
        self.user: get_user_model
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Jon 1953-2021", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)

    def test_endpoint(self):
        """Test endpoint"""
        client = Client()
        response = client.get("/DB/")
        self.assertEqual(200, response.status_code)

    def test_show_estate(self):
        """Test show estate"""
        client = Client()
        response = client.get("/DB/")
        self.assertContains(response, "Jon 1953-2021")
