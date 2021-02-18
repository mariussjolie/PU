import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Estate


# Create your tests here.


class EstateUnitTest(TestCase):

    def setUp(self):
        self.user: get_user_model
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Solfrid 90", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)

    def test_address(self):
        self.assertEqual("Trondheim", self.test_estate.address)

    def test_title(self):
        self.assertEqual("Solfrid 90", self.test_estate.title)

    def test_user(self):
        self.assertEqual(self.user, self.test_estate.users.get())
