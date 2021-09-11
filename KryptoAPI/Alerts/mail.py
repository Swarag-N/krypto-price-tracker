from django.core.mail import EmailMessage
from django.conf import settings


def send_update_email(email, subject,message):

    email_subject = subject
    email_body = message

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)