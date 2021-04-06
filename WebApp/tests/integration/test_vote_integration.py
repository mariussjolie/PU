"""Module containing Integration test for estate"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate, Item, Vote


# Create your tests here.


class EstateIntegrationTest(TestCase):
    """Estate Integration Test"""

    def setUp(self):
        """Set up test objects"""
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Jon 1953-2021", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)
        self.test_item = Item.objects.create(id=1, description="test_item", estate=self.test_estate)
        self.test_item.save()

    def test_endpoint(self):
        """Test endpoint"""
        client = Client()
        response = client.get("/estates/1/")
        self.assertEqual(403, response.status_code)
        response = client.post("/estates/1/")
        self.assertEqual(403, response.status_code)

        client.login(username="username123", password="password123")
        response = client.get("/estates/1/")
        self.assertEqual(200, response.status_code)

    def test_show_votes(self):
        """Test show votes"""
        client = Client()
        client.login(username="username123", password="password123")
        response = client.get("/estates/1/")
        self.assertContains(response, "test_item")

    def test_submit_votes(self):
        """Test vote form submission"""
        data = {
            "form-INITIAL_FORMS": 1,
            "form-TOTAL_FORMS": 1,
            "form-0-importance": 4,
            "form-0-choice": "donate",
            "form-0-id": 1,
        }
        client = Client()
        client.login(username="username123", password="password123")
        client.get("/estates/1/")
        response = client.post("/estates/1/", data=data)
        self.assertEqual(200, response.status_code)
        vote = Vote.objects.get(id=1)
        self.assertEqual(vote.importance, 4)
        self.assertEqual(vote.choice, 'donate')
