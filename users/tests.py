from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase
from django.urls import reverse

from users.views import logout_request

from .forms import ProfileForm, UserForm
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
        self.assertRedirects(response, reverse("users:homepage"))


class SignUpTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_success(self):
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone_number": "+380980437157",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users:homepage"))
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertTrue(Profile.objects.filter(phone_number="+380980437157").exists())
        self.assertTrue(Profile.objects.filter(role="VI").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Registration successful.")

    def test_sign_up_invalid_information_u_f(self):
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "testuser",
                "password1": "test",
                "password2": "test",
                "phone_number": "+380980437157",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unsuccessful registration. Invalid information.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_sign_up_invalid_information_p_f(self):
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone_number": "+3809804371571",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unsuccessful registration. Invalid information.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_sign_up_existing_phone_number(self):
        user = User.objects.create_user(username="existinguser", password="testpassword")
        Profile.objects.create(
            user_id=user.id, phone_number="+380980437157", role="VI"
        )
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone_number": "+380980437157",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The number is already registered or invalid.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_sign_up_existing_user(self):
        user = User.objects.create_user(username="existinguser", password="testpassword")
        Profile.objects.create(
            user_id=user.id, phone_number="+380980437157", role="VI"
        )
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "existinguser",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone_number": "+380980437155",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unsuccessful registration. Invalid information.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_sign_up_non_ukraine_code(self):
        response = self.client.post(
            reverse("users:sign-up"),
            {
                "username": "existinguser",
                "password1": "testpassword",
                "password2": "testpassword",
                "phone_number": "+33612345678",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter the telephone number of Ukraine.")
