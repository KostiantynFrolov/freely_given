from django.conf import settings
from django.core.mail import send_mail

def send_confirmational_email(user):
    send_mail(
    subject="Witamy na naszej stronie!",
    message="Dziękujemy, że do nas dołączyłeś!",
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[user.username],
    fail_silently=False)
