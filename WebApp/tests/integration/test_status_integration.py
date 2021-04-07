"""Module containing Integration test for estate"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate, Item, Vote


class StatusIntegrationTest(TestCase):
    """Estate Integration Test"""

    # pylint: disable=invalid-name
    def setUp(self):
        """Set up test objects"""
        self.user1 = get_user_model().objects.create_user(
            "username1", "email1@email.com", "password123")
        self.user2 = get_user_model().objects.create_user(
            "username2", "email2@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1,
            address="Trondheim",
            title="Jon 1953-2021",
            date=datetime.datetime(
                2015,
                10,
                9,
                23,
                55,
                59,
                342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user1)
        self.test_estate.users.add(self.user2)
        self.item1 = Item.objects.create(
            description="Hus", estate=self.test_estate)
        self.item2 = Item.objects.create(
            description="Bil", estate=self.test_estate)
        self.admin = get_user_model().objects.create_superuser(
            "admin", "admin@admin.no", "password123")
        self.vote_user1 = Vote.objects.create(
            item=self.item1, user=self.user1, choice="throw", importance="7")
        self.vote_user2 = Vote.objects.create(
            item=self.item2, user=self.user2, choice="keep", importance="10")

    def test_endpoint(self):
        """Test endpoint"""
        client = Client()
        response = client.get("/estates/1/adminoverview/")
        self.assertEqual(302, response.status_code)
        client.force_login(self.admin)
        response = client.get("/estates/1/adminoverview/")
        self.assertEqual(200, response.status_code)

    def test_show_estate(self):
        """Test show estate"""
        client = Client()
        client.force_login(self.admin)
        response = client.get("/estates/1/adminoverview/")
        self.assertContains(response, "Jon 1953-2021")
