import string
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_password(password):
    if not any(symbol.isupper() for symbol in password):
        raise ValidationError("To hasło musi zawierać co najmniej jedną wielką literę.")
    if not any(char.islower() for char in password):
        raise ValidationError("To hasło musi zawierać co najmniej jedną małą literę.")
    if not any(elem.isdigit() for elem in password):
        raise ValidationError("To hasło ma zawierać co najmniej jedną cyfrę.")
    if not any(item in string.punctuation for item in password):
        raise ValidationError("To hasło ma zawierać co najmniej jeden znak specjalny.")
    return password


class ResetPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["placeholder"] = "Hasło"
        self.fields["password2"].widget.attrs["placeholder"] = "Powtórz hasło"

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        return validate_password(password1)


class RegisterForm(ResetPasswordForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Imię"
        self.fields["last_name"].widget.attrs["placeholder"] = "Nazwisko"
        self.fields["username"].widget.attrs["placeholder"] = "Email"


class PasswordConfirmForm(forms.Form):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

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


class CustomPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        return validate_password(new_password1)



