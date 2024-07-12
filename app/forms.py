import string
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Donation, Institution


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
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        "placeholder": "Hasło"}))


class LoginForm(PasswordConfirmForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Email"
    }))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Email"


class CustomPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get("new_password1")
        return validate_password(new_password1)


class SendMailToSuperusersForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Imię"}))
    surname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Nazwiśko"}))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 1, "placeholder": "Wiadomość"}))


class AddDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ("user",)
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
            "pick_up_date": forms.DateInput(attrs={"type": "date"}),
            "pick_up_time": forms.TimeInput(attrs={"type": "time"}),
            "pick_up_comment": forms.Textarea(attrs={"rows": 5})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs.update({
            "min": "1", "value": "1"})

    def get_full_institution_data(self):
        institutions_all = Institution.objects.all()
        institutions_categories = [list(institution.categories.all().values_list('id', flat=True))
                                   for institution in institutions_all]
        institutions_full_data = zip(institutions_all, institutions_categories)
        return institutions_full_data










