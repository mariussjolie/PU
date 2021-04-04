"""Module containing Estate unit test"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Estate


# Create your tests here.


class EstateUnitTest(TestCase):
    """Unit test for Estate"""

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

    def test_address(self):
        """Test address"""
        self.assertEqual("Trondheim", self.test_estate.address)

    def test_title(self):
        """Test title"""
        self.assertEqual("Jon 1953-2021", self.test_estate.title)

    def test_user(self):
        """Test user"""
        self.assertEqual(self.user, self.test_estate.users.get())
