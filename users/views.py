from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import LoginForm, PhoneNumberForm, UserForm
from .models import VISITOR, Profile


def home(request):
    return render(request, "home.html")


def register_request(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = PhoneNumberForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            phone_number = profile_form.cleaned_data.get("phone_number")
            profile = Profile(user=user, phone_number=phone_number, role=VISITOR)
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("users:homepage")
        else:
            if not profile_form.is_valid():
                messages.error(request, "The number is already registered or invalid")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        user_form = UserForm()
        profile_form = PhoneNumberForm()
    return render(
        request=request,
        template_name="sign_up.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            try:
                profile = Profile.objects.get(phone_number=phone_number)
            except Profile.DoesNotExist:
                messages.error(request, "Invalid phone number.")
                form = LoginForm()
                return render(
                    request=request,
                    template_name="sign_in.html",
                    context={"form": form},
                )
            user = User.objects.get(id=profile.user_id)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")
                return redirect("users:homepage")
            else:
                messages.error(request, "Invalid phone number or password.")
        else:
            messages.error(request, "Invalid phone number or password.")
    form = LoginForm()
    return render(request=request, template_name="sign_in.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("users:homepage")
