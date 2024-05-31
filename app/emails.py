from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_confirmational_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)

    subject = "Witamy na naszej stronie!"
    activation_link = f"http://{current_site}{reverse('account_activation', kwargs={'uid': uid, 'token': token})}"
    message = f"Dziękujemy, że do nas dołączyłeś!\n Aby aktywować konto, kliknij w link poniżej.\n\n {activation_link} "
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])


