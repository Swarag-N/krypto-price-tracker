from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KryptoAPI.settings')

app = Celery('KryptoAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'get_latest_price_of_BTC',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'