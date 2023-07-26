import phonenumbers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse

from .forms import SignInForm, SignUpForm
from .models import VISITOR, Profile


def base(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    return render(
        request, "base/base.html", {"signup_url": signup_url, "login_url": login_url}
    )


def home(request):
    return render(request, "home.html")


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get("email")
            if User.objects.filter(username=user_email).exists():
                messages.error(request, "Registration failed. Email already exists.")
            else:
                user = form.save(commit=False)
                user.username = user_email
                profile = Profile(user=user, role=VISITOR)
                user.save()
                profile.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("site:home")
    else:
        form = SignUpForm()
    return render(
        request=request,
        template_name="sign_up.html",
        context={"form": form},
    )


def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get("email")
            user_password = form.cleaned_data.get("password")
            user = authenticate(username=user_email, password=user_password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.email}.")
                return redirect("site:home")
            else:
                messages.error(request, "Wrong email or password.")
        else:
            messages.error(request, "Enter a valid email address.")
    form = SignInForm()
    return render(request=request, template_name="sign_in.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("site:home")
