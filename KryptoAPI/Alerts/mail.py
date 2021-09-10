from django.core.mail import EmailMessage
from django.conf import settings


def send_update_email(email, message):

    email_subject = 'Here is you status review'
    email_body = message

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)