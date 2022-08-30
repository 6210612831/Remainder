from .models import *
from django.shortcuts import render, get_object_or_404
import requests
import Remainder.settings as setting
from rest_framework import status

def index(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/task', headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})
    if response.status_code == status.HTTP_200_OK:
        return render(request, "task/index.html",{'task_list':response.json()})
    else:
        return render(request, "task/index.html",{'task_list':[]})