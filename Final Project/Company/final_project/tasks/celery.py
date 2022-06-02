from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
from random import randint
import os

os.environ.setdefault( value='final_project.settings', key ='DJANGO_SETTINGS_MODULE',)
app = Celery('final_project', broker='amqp://127.0.0.1:5672')

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Tashkent')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

hours = randint(1,3)
cost = randint(5,50)
area = randint(40,200)

app.conf.beat_schedule = {
    'calculate': {
        'task': 'final_project.tasks.tasks.test_calculate',
        'schedule': 30,
        'args': (cost, area, hours)
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
