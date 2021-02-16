from django.test import Client, TestCase
from django.contrib.auth import get_user_model

class UserIntegrationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("testuser", "test@test.com", "testpassword")

    def test_endpoints(self):
        """Test user endpoints returns 200 ok"""
        c = Client()
        response = c.get("/auth/login/")
        self.assertEqual(200, response.status_code)
        response = c.get("/auth/signup/")
        self.assertEqual(200, response.status_code)

    def test_login(self):
        """Test login"""
        c = Client()
        response = c.post("/auth/login/", {"username": "testuser", "password": "testpassword"})
        self.assertEqual(302, response.status_code)
        response = c.get("/")
        self.assertContains(response, "Hi testuser!")
        c = Client()
        response = c.post("/auth/login/", {"username": "testuser", "password": "testWrongPassword"})
        self.assertNotEqual(302, response.status_code)
        response = c.get("/")
        self.assertNotContains(response, "Hi testuser!")
        response = c.post("/auth/login/", {"username": "admin", "password": "admin123"})
        self.assertNotEqual(302, response.status_code)
        self.assertTrue(c.login(username="testuser", password="testpassword"))

    def test_logout(self):
        """Test logout"""
        c = Client()
        c.post("/auth/login/", {"username": "testuser", "password": "testpassword"})
        response = c.get('/')
        self.assertContains(response, "Hi testuser!")
        response = c.get("/auth/logout/")
        self.assertContains(response, "Logged out")
        response = c.get('/')
        self.assertNotContains(response, "Hi testuser!")

    def test_signup(self):
        """Test signup"""
        c = Client()
        response = c.post("/auth/signup/", {"username": "test_user123", "email": "test@testmail.com",
                                            "password1": "testpass123", "password2": "testpass123"})
        self.assertEqual(302, response.status_code)

    def test_login_after_signup(self):
        """Test signup, then login with same credentials"""
        c = Client()
        response = c.post("/auth/signup/", {"username": "test_user123", "email": "testmail@test.com",
                                            "password1": "testpass123", "password2": "testpass123"})
        self.assertEqual(302, response.status_code)
        response = c.post("/auth/login/", {"username": "test_user123", "password": "testpass123"})
        self.assertEqual(302, response.status_code)
        self.assertTrue(c.login(username="test_user123", password="testpass123"))
