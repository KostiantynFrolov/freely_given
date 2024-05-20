from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["placeholder"] = "Imię"
        self.fields["last_name"].widget.attrs["placeholder"] = "Nazwisko"
        self.fields["username"].widget.attrs["placeholder"] = "Email"
        self.fields["password1"].widget.attrs["placeholder"] = "Hasło"
        self.fields["password2"].widget.attrs["placeholder"] = "Powtórz hasło"


class PasswordConfirmForm(forms.Form):
    password = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["placeholder"] = "Hasło"


class LoginForm(PasswordConfirmForm):
    username = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Email"
