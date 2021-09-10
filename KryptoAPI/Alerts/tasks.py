from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from KryptoAPI.celery import app

from Alerts.helpers.requests_manager import get_bitcoin_price
from Alerts.helpers.db_handler import send_updates
from Alerts.mail import send_update_email


logger = get_task_logger(__name__);




@app.task(name="send_review_email_task")
def send_email_task(email, message):
    logger.info("update email to "+email);
    return send_update_email(email, message)


@app.task(name="price_updates")
def price_updates():
    try:
        BTC_PRICE = get_bitcoin_price()
        users = send_updates(BTC_PRICE)
        for i in users:
            send_email_task.delay(i.get('recepinet'),i.get('body'))        
    except Exception as e:
        logger.error(str(e))


# def mail(email=None, message=None, subject=None):
#     send_mail(subject=subject, message=message, recipient_list=[email], from_email=settings.EMAIL_HOST_USER)