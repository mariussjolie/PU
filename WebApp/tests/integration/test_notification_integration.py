"""Module containing Integration test for notification"""

import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate, Notify


# Create your tests here.


class NotificationIntegrationTest(TestCase):
    """Estate Integration Test"""

    def setUp(self):
        """Set up test objects"""
        self.user1 = get_user_model().objects.create_user(
            "username1", "email1@email.com", "password123")
        self.user2 = get_user_model().objects.create_user(
            "username2", "email2@email.com", "password123")
        self.test_estate = Estate.objects.create(
            id=1, address="Trondheim", title="Solfrid 90", date=datetime.datetime(
                2015, 10, 9, 23, 55, 59, 342380))
        self.test_estate.save()
        self.test_estate.users.add(self.user1)
        self.test_estate.users.add(self.user2)
        self.admin = get_user_model().objects.create_superuser("admin", "admin@admin.no", "password123")
        self.test_notification = Notify.objects.create(user_id=self.user1.id, estate_id=self.test_estate.id)
        self.test_notification.save()
    '''
    def test_endpoint(self):
        """Test endpoint"""
        client = Client()
        response = client.get("admin_view_estate_item1/1/1/notify/1/")
        self.assertEqual(403, response.status_code)
        self.assertRaises(Notify.DoesNotExist, Notify.objects.get, user__id=2, estate__id=self.test_estate.id)
        client.force_login(self.admin)
        response = client.get("admin_view_estate_item1/1/1/notify/1/")
        self.assertEqual(302, response.status_code)
        self.assertTrue(Notify.objects.get(user__id=2, estate__id=self.test_estate.id))
    '''