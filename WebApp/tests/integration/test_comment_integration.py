"""Module containing Integration test for estate"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from WebApp.models import Estate, Item, Comment


# Create your tests here.


class EstateIntegrationTest(TestCase):
    """Estate Integration Test"""

    # pylint: disable=invalid-name
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
        self.test_comment = Comment.objects.create(id=1, user=self.user, item=self.test_item, comment="testkommentar123")

    def test_show_comment(self):
        """Test show votes"""
        client = Client()
        client.login(username="username123", password="password123")
        response = client.get("/estates/1/1/")
        self.assertContains(response, "testkommentar123")

    def test_submit_comment(self):
        """Test Comment submit"""
        data = {
            "comment": "DETTE ER EN KOMMENTAR"
        }
        client = Client()
        client.login(username="username123", password="password123")
        response = client.post("/estates/1/1/addcomment", data=data)
        self.assertEqual(302, response.status_code)
        comment = Comment.objects.get(id=2)
        self.assertEqual(self.user, comment.user)
        self.assertEqual(self.test_item, comment.item)
        self.assertEqual("DETTE ER EN KOMMENTAR", comment.comment)
