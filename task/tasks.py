from __future__ import absolute_import, unicode_literals
from celery import shared_task
from task.models import Task
from datetime import datetime
from django.utils import timezone
import requests
TOKEN = 'Bearer VaQiVzn5SqjJysdYSblOaJuS5xCBDw3qucIfzmJPyI5'









@shared_task
def line_alert(task_name):
    global TOKEN
    requests.post("https://notify-api.line.me/api/notify",headers={'Authorization': TOKEN},data={"message":f"This is your task that due : {task_name}"})
    return "Done line_alert()"

