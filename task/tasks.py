from __future__ import absolute_import, unicode_literals
from celery import shared_task
from task.models import Task
from datetime import datetime
from django.utils import timezone
import requests
TOKEN = 'Bearer VaQiVzn5SqjJysdYSblOaJuS5xCBDw3qucIfzmJPyI5'



@shared_task
def check_time():
    count_call_alert_function = 0
    task_name = ""
    for x in Task.objects.filter(active = True):
        if x.time  <= timezone.now():
            if task_name != "":
                task_name += ","
            task_name += str(x.name)
            count_call_alert_function += 1
            if x.repeat == False:
                x.active = False
                x.save()
    global TOKEN
    res = requests.post("https://notify-api.line.me/api/notify",headers={'Authorization': TOKEN},data={"message":f"This is your task that due : {task_name}"})
    return f"CALL ALERT FUNCTION {count_call_alert_function} TIMES"





