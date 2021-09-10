from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from KryptoAPI.celery import app

from Alerts.helper import get_bitcoin_price
from Alerts.mail import send_update_email

from django.conf import settings
from django.core.mail import send_mail


logger = get_task_logger(__name__);


@app.task(name="price_updates")
def price_updates():
    try:
        logger.info(get_bitcoin_price())
        send_update_email("swarag",'narayanasetty.swarag2018@vitstudent.ac.in',"sddsd");
    except Exception as e:
        print(e)


# def mail(email=None, message=None, subject=None):
#     send_mail(subject=subject, message=message, recipient_list=[email], from_email=settings.EMAIL_HOST_USER)