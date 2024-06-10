from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_confirmational_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    subject = "Witamy na naszej stronie!"
    activation_link = f"http://{settings.ALLOWED_HOSTS[-1]}:8000{reverse('account_activation', kwargs={'uid': uid, 'token': token})}"
    message = f"Dziękujemy, że do nas dołączyłeś!\nAby aktywować konto, kliknij w link poniżej.\n\n {activation_link} "
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])


def send_password_reset_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    subject = "Resetowanie hasła"
    reset_password_link = f"http://{settings.ALLOWED_HOSTS[-1]}:8000{reverse('reset_password', kwargs={'uid': uid, 'token': token})}"
    message = f"Aby zmienić hasło, kliknij w link poniżej.\n\n {reset_password_link} "
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])


