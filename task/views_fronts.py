from .models import *
from django.shortcuts import render, get_object_or_404
import requests
import Remainder.settings as setting
from rest_framework import status
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.urls import reverse

HOST = "https://reminder-white.herokuapp.com"
# HOST = "http://127.0.0.1:8000"


def index(request):
    response = requests.get(f'{HOST}/api/v1/task', json={'user_id':str(request.user.id)}, headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})
    if response.status_code == status.HTTP_200_OK:
        return render(request, "task/index.html",{'task_list':response.json()})
    else:
        return render(request, "task/index.html",{'task_list':[]})

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("task:index"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("task:index"))
        else:
            return HttpResponseRedirect(reverse("task:index"))
    return HttpResponseRedirect(reverse("task:index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("task:index"))
