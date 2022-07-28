from .celery import app as celery_app
from django.core.mail import send_mail

__all__ = ('celery_app',)


