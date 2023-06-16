from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase
from django.urls import reverse

from users.views import logout_request

User = get_user_model()


class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("users:homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")


class LogoutViewTest(TestCase):
    def test_logout_view(self):
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
