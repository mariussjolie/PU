import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Estate, Notify


class NotifyUnitTest(TestCase):
    """Unit test for Estate"""

    def setUp(self):
        """Set up test objects"""
        self.user = get_user_model().objects.create_user(
            "username123", "email@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Solfrid 90", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user)
        self.test_notification = Notify.objects.create(user_id=self.user.id, estate_id=self.test_estate.id)
        self.test_notification.save()

    def test_notification_exists(self):
        """Test adress"""
        self.assertEqual(self.test_notification,
                         Notify.objects.get(user__id=self.user.id, estate__id=self.test_estate.id))