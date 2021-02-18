"""User integration test module"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class UserIntegrationTest(TestCase):
    """User integration test"""
    def setUp(self):
        """Set up object for testing"""
        self.user = get_user_model().objects\
            .create_user("testuser", "test@test.com", "testpassword")

    def test_endpoints(self):
        """Test user endpoints returns 200 ok"""
        client = Client()
        response = client.get("/auth/login/")
        self.assertEqual(200, response.status_code)
        response = client.get("/auth/signup/")
        self.assertEqual(200, response.status_code)

    def test_login(self):
        """Test login"""
        client = Client()
        response = client.post("/auth/login/",
                               {"username": "testuser", "password": "testpassword"})
        self.assertEqual(302, response.status_code)
        response = client.get("/")
        self.assertContains(response, "Hi testuser!")
        client = Client()
        response = client.post("/auth/login/",
                               {"username": "testuser", "password": "testWrongPassword"})
        self.assertNotEqual(302, response.status_code)
        response = client.get("/")
        self.assertNotContains(response, "Hi testuser!")
        response = client.post("/auth/login/",
                               {"username": "admin", "password": "admin123"})
        self.assertNotEqual(302, response.status_code)
        self.assertTrue(client.login(username="testuser", password="testpassword"))

    def test_logout(self):
        """Test logout"""
        client = Client()
        client.post("/auth/login/", {"username": "testuser", "password": "testpassword"})
        response = client.get('/')
        self.assertContains(response, "Hi testuser!")
        response = client.get("/auth/logout/")
        self.assertContains(response, "Logged out")
        response = client.get('/')
        self.assertNotContains(response, "Hi testuser!")

    def test_signup(self):
        """Test signup"""
        client = Client()
        response = client.post("/auth/signup/",
                               {"username": "test_user123",
                                "email": "test@testmail.com",
                                "password1": "testpass123",
                                "password2": "testpass123"})
        self.assertEqual(302, response.status_code)

    def test_login_after_signup(self):
        """Test signup, then login with same credentials"""
        client = Client()
        response = client.post("/auth/signup/",
                               {"username": "test_user123",
                                "email": "testmail@test.com",
                                "password1": "testpass123",
                                "password2": "testpass123"})
        self.assertEqual(302, response.status_code)
        response = client.post("/auth/login/",
                               {"username": "test_user123", "password": "testpass123"})
        self.assertEqual(302, response.status_code)
        self.assertTrue(client.login(username="test_user123", password="testpass123"))
