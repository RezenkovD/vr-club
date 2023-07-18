from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase
from django.urls import reverse

from users.views import logout_request

from .forms import SignUpForm
from .models import Profile
from .views import sign_up


class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("users:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class LogoutViewTest(TestCase):
    def test_logout_view(self):
        User = get_user_model()
        client = Client()
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        client.force_login(user)
        response = client.get(reverse("users:homepage"))
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        response = client.get(reverse("users:logout"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "You have successfully logged out.")
        self.assertRedirects(response, reverse("site:home"))


class SignUpTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.first_name = "first_name"
        self.last_name = "last_name"
        self.email = "testuser@example.com"
        self.username = "testuser@example.com"
        self.password = "testpassword"
        self.role = "VI"

    # def test_sign_up_success(self):
    #     response = self.client.post(
    #         reverse("users:sign-up"),
    #         {
    #             "first_name": self.first_name,
    #             "last_name": self.last_name,
    #             "email": self.email,
    #             "password1": self.password,
    #             "password2": self.password,
    #         },
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("site:home"))
    #     self.assertTrue(User.objects.filter(username=self.email).exists())
    #     self.assertTrue(Profile.objects.filter(user__username=self.email).exists())
    #     self.assertTrue(Profile.objects.filter(role=self.role).exists())
    #     messages = list(get_messages(response.wsgi_request))
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), "Registration successful.")

    # def test_sign_up_invalid_information(self):
    #     response = self.client.post(
    #         reverse("users:sign-up"),
    #         {
    #             "email": self.email,
    #             "password1": "testpassword",
    #             "password2": "testpassword",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "This field is required.")
    #     self.assertFalse(User.objects.filter(username=self.email).exists())

    def test_sign_up_existing_user(self):
        User.objects.create_user(username=self.email, password=self.password)
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registration failed. Email already exists.")
        self.assertFalse(User.objects.filter(email=self.email).exists())


class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "testuser@example.com"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.email, password=self.password
        )

    def test_sign_in_valid_credentials(self):
        response = self.client.post(
            reverse("users:sign-in"),
            {"email": self.email, "password": self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("site:home"))
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_sign_in_invalid_credentials(self):
        response = self.client.post(
            reverse("users:sign-in"),
            {"email": self.email, "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrong email or password.")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_sign_in_unregistered_email(self):
        response = self.client.post(
            reverse("users:sign-in"),
            {"email": "unregistered@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrong email or password.")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_sign_in_invalid_form(self):
        response = self.client.post(
            reverse("users:sign-in"),
            {"email": "invalidemail", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.")
        self.assertFalse("_auth_user_id" in self.client.session)
