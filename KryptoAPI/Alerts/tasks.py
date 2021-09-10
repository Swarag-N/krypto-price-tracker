from __future__ import absolute_import, unicode_literals
from os import name
from celery import shared_task
from KryptoAPI.celery import app

from django.conf import settings
from django.core.mail import send_mail
import requests


@app.task(name="get_latest_price_of_BTC")
def get_latest_price_of_BTC():
    try:
        prices = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
        cur_price=(prices[0]['current_price'])
        print(cur_price)
        print("*******************************************")
    except Exception as e:
        print(e)


# def mail(email=None, message=None, subject=None):
#     send_mail(subject=subject, message=message, recipient_list=[email], from_email=settings.EMAIL_HOST_USER)