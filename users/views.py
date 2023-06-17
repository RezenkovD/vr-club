import phonenumbers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignInForm, UserForm
from .models import VISITOR, Profile


def home(request):
    return render(request, "home.html")


def sign_up(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            phone_number = profile_form.cleaned_data.get("phone_number")
            if phonenumbers.parse(str(phone_number), "UA").country_code != 380:
                messages.error(request, "Enter the telephone number of Ukraine.")
                messages.error(
                    request, "Unsuccessful registration. Invalid information."
                )
            else:
                user = user_form.save()
                profile = Profile(user=user, phone_number=phone_number, role=VISITOR)
                profile.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("users:homepage")
        else:
            if not profile_form.is_valid():
                messages.error(request, "The number is already registered or invalid.")
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request=request,
        template_name="sign_up.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )


def sign_in(request):
    if request.method == "POST":
        sign_in = SignInForm(request.POST)
        if sign_in.is_valid():
            phone_number = sign_in.cleaned_data.get("phone_number")
            password = sign_in.cleaned_data.get("password")
            try:
                profile = Profile.objects.get(phone_number=phone_number)
            except Profile.DoesNotExist:
                messages.error(request, "The phone number is not registered.")
                sign_in = SignInForm()
                return render(
                    request=request,
                    template_name="sign_in.html",
                    context={"sign_in": sign_in},
                )
            user = User.objects.get(id=profile.user_id)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.username}.")
                return redirect("users:homepage")
            else:
                messages.error(request, "Wrong phone number or password.")
        else:
            messages.error(request, "Invalid phone number or password.")
    sign_in = SignInForm()
    return render(
        request=request, template_name="sign_in.html", context={"sign_in": sign_in}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("users:homepage")
