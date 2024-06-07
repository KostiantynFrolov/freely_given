import string

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not any(symbol.isupper() for symbol in password1):
            raise ValidationError("To hasło musi zawierać co najmniej jedną wielką literę.")
        if not any(char.islower() for char in password1):
            raise ValidationError("To hasło musi zawierać co najmniej jedną małą literę.")
        if not any(elem.isdigit() for elem in password1):
            raise ValidationError("To hasło ma zawierać co najmniej jedną cyfrę.")
        if not any(item in string.punctuation for item in password1):
            raise ValidationError("To haso ma zawierać co najmniej jeden znak specjalny.")
        return password1


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


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Email"
