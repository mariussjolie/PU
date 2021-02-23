"""Module containing Unit test for Vote"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Vote, Estate, Item


class VoteUnitTest(TestCase):
    """Unit test for Vote Class"""

    def setUp(self):
        """Setup test-objects"""
        self.user: get_user_model
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Solfrid 90", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)

        self.test_item = Item.objects.create(
            id=1, estate=self.test_estate, description="Stol med brukket ben")
        self.test_item.save()

        self.test_vote = Vote.objects.create(
            id=1, user=self.user, item=self.test_item, choice="Keep", importance="1")
        self.test_vote.save()

    def test_choice(self):
        """Test vote choice"""
        self.assertEqual("Keep", self.test_vote.choice)
