from django.urls import path
from .views import home, sign_up

urlpatterns = [
    path("", home),
    path("sign-up/", sign_up),
]
