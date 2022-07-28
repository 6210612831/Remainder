from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django_celery_beat.models import PeriodicTask as Task
from django.core.mail import send_mail


@shared_task
def send_email(**kwargs):
    obj = Task.objects.get(id=int(kwargs['task_id']))
    
    send_mail(
    'Task alert !!',
    f'Your task {obj.name} start at {obj.start_time}',
    'monday25436@gmail.com',
    [f"{kwargs['email']}"],
    fail_silently=False,
    )
    return f"call function send_email() from monday25436@gmail.com to {kwargs['email']}"
