from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField
from phonenumber_field.modelfields import PhoneNumberField

from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    class Meta:
        model = Profile
        fields = ("phone_number",)


class SignInForm(forms.Form):
    phone_number = PhoneNumberFormField(widget=forms.TextInput(), required=False)
    password = forms.CharField(max_length=32)
