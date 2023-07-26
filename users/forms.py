from allauth.account.forms import SignupForm, LoginForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=32, required=True, label="Name")

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input-field", "placeholder": ""})


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input-field", "placeholder": ""})
