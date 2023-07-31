from django import forms
from phonenumber_field.formfields import PhoneNumberField as PhoneNumberFormField

from .models import BookingTime


class BookingForm(forms.Form):
    name = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    phone_number = PhoneNumberFormField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    number_of_people = forms.IntegerField(min_value=1)
    comment = forms.CharField(
        max_length=256,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    slots = forms.MultipleChoiceField(
        choices=BookingTime.TIME_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
