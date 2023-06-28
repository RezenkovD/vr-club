from django import forms
from .models import BookingTime


class BookingForm(forms.Form):
    comment = forms.CharField(
        max_length=128, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    slots = forms.MultipleChoiceField(
        choices=BookingTime.TIME_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=True,
    )
