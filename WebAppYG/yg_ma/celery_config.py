from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yg_ma.settings')

app = Celery('yg_ma')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()