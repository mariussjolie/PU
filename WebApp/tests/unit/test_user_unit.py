"""Module for User Unit Test"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class UserUnitTest(TestCase):
    """Unit test for User class"""

    def setUp(self):
        """Set up objects for testing"""
        self.user: get_user_model
        self.user = get_user_model().objects \
            .create_user("username123", "email@email.com", "password123")

    def test_username(self):
        """Test username"""
        self.assertEqual("username123", self.user.get_username())

    def test_password(self):
        """Test password"""
        self.assertTrue(self.user.check_password("password123"))
        self.assertTrue(self.user.has_usable_password())
        self.user.set_password("test123")
        self.assertFalse(self.user.check_password("password123"))
        self.user.set_unusable_password()
        self.assertFalse(self.user.has_usable_password())

    def test_email(self):
        """Test email"""
        self.assertEqual("email@email.com", self.user.email)
