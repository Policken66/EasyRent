from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyRent.settings')

app = Celery('EasyRent')

# Используйте строку конфигурации для Redis
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживает все задачи (tasks.py) в каждом из приложений
app.autodiscover_tasks()