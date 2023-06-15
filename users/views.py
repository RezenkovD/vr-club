import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .forms import UserForm
from .utils import is_valid_password


# Create your views here.
def home(request):
    return render(request, "home.html")


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            errors = is_valid_password(password)
            if not errors:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                user.password = hashed_password
                user.save()
                email = form.cleaned_data.get("email")
                messages.success(request, f"Account created for {email}")
                return redirect(to="/users")
            else:
                for error in errors:
                    form.add_error("password", error)
    else:
        form = UserForm()
    return render(request, "sign_up.html", {"form": form})
