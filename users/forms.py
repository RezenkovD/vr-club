from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField
from phonenumber_field.modelfields import PhoneNumberField

from .models import Profile


class UserForm(UserCreationForm):
    username = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
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
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class PhoneNumberForm(forms.ModelForm):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    class Meta:
        model = Profile
        fields = ["phone_number"]


class LoginForm(forms.Form):
    phone_number = PhoneNumberFormField(widget=forms.TextInput(), required=False)
    password = forms.CharField(max_length=32)
