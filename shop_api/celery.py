import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

# Create the Celery app
app = Celery('shop_api')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all registered Django apps
app.autodiscover_tasks()

# Define periodic tasks
app.conf.beat_schedule = {
    'send-hourly-greeting': {
        'task': 'users.tasks.send_hourly_greeting',
        'schedule': crontab(minute=0),  # Execute at the start of every hour
    },
}