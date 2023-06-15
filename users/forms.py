from django.forms import ModelForm
from .models import User


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
