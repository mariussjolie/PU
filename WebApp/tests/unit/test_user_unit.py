from django.test import TestCase
from django.contrib.auth import get_user_model


class UserUnitTest(TestCase):
    def setUp(self):
        self.user: get_user_model
        self.user = get_user_model().objects.create_user("username123", "email@email.com","password123")

    def test_username(self):
        self.assertEqual("username123", self.user.get_username())

    def test_password(self):
        self.assertTrue(self.user.check_password("password123"))
        self.assertTrue(self.user.has_usable_password())
        self.user.set_password("test123")
        self.assertFalse(self.user.check_password("password123"))
        self.user.set_unusable_password()
        self.assertFalse(self.user.has_usable_password())

    def test_email(self):
        self.assertEqual("email@email.com", self.user.email)



