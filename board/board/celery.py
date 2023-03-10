import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board.settings')

app = Celery('board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_mail_every_week': {
        'task': 'news.tasks.mail_spam',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}