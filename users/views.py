import phonenumbers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignInForm, SignUpForm
from .models import VISITOR, Profile


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
                return redirect("site:home")
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
    return redirect("site:home")
