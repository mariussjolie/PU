"""Module containing Item Unit test"""
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from WebApp.models import Estate, Item, Comment


class CommentUnitTest(TestCase):
    """Unit test for Comment"""

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

        self.item = Item.objects.create(
            id=1, estate=self.test_estate, description="Old chair")
        self.item.save()
        self.comment = Comment.objects.create(id=1, item=self.item, user=self.user, comment="kommentar123")
        self.comment.save()

    def test_content(self):
        """Test comment content"""
        self.assertEqual("kommentar123", self.comment.comment)

    def test_user(self):
        """Test comment user"""
        self.assertEqual(self.user, self.comment.user)
    def test_item(self):
        """Test comment item"""
        self.assertEqual(self.item, self.comment.item)
