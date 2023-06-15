from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import UserForm, ProfileForm
from .utils import is_valid_password
from .models import Profile


def home(request):
    return render(request, "home.html")


def register_request(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            password = user_form.cleaned_data.get("password1")
            errors = is_valid_password(password)
            if not errors:
                user = user_form.save()
                phone_number = profile_form.cleaned_data.get("phone_number")
                profile = Profile(user=user, phone_number=phone_number)
                profile.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("main:homepage")
            else:
                for error in errors:
                    user_form.add_error("password1", error)
        else:
            if not profile_form.is_valid():
                messages.error(request, "The number is already registered or invalid")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request=request,
        template_name="sign_up.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="sign_in.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")
