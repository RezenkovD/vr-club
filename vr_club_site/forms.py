from django import forms

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
    date = forms.DateField(
        required=True,
        input_formats=["%d-%m-%Y"],
        widget=forms.DateInput(
            format="%d-%m-%Y",
            attrs={
                "class": "form-control",
            },
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
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    people_count = forms.IntegerField(min_value=1)  # TODO: rename to people_count
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
