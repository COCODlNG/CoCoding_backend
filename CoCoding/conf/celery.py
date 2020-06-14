from celery import Celery
from django.conf import settings
import os


CELERY_IMPORTS = (
    'tasks.run_code',
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf', broker=settings.CELERY_BROKER_URL, include=CELERY_IMPORTS)


app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
