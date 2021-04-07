"""Module containing Item Unit test"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Estate, Item


class ItemUnitTest(TestCase):
    """Unit test for Item"""

    # pylint: disable=invalid-name
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

        self.test_item = Item.objects.create(
            id=1, estate=self.test_estate, description="Old chair")
        self.test_item.save()

    def test_description(self):
        """Test Item description"""
        self.assertEqual("Old chair", self.test_item.description)
