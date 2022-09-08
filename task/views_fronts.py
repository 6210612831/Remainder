from ast import arg
import re
from .models import *
from django.shortcuts import render, get_object_or_404
import requests
import Remainder.settings as setting
from rest_framework import status
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from django.urls import reverse

HOST = "http://127.0.0.1:8000"



def test(request):
    return HttpResponseRedirect(reverse("task:index", kargs={'testtest':'wdadwdadadwa'}))

def index(request):
    if request.user.id is None:
        return render(request, "task/index.html",{'task_list':[]})
    else:
        response = requests.get(f'{HOST}/api/v1/task', json={'user_id':str(request.user.id)}, headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})
        if response.status_code == status.HTTP_200_OK:
            return render(request, "task/index.html",{'task_list':response.json() if len(response.json()) != 0 else []})
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
            response = requests.get(f'{HOST}/api/v1/task', json={'user_id':str(user.id)}, headers={"Authorization": f"Bearer {setting.REMAINDER_TOKEN}"})  
            return render(request, "task/index.html",{'task_list':response.json() if len(response.json()) != 0 else [],'login_message':'Login Succress'})
        else:
            return render(request, "task/index.html",{'task_list':[],'login_message':'Wrong username or password'})
    return HttpResponseRedirect(reverse("task:index"))

def register(request):
    # Check this view use when call register page or use when submit register form
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        # email = request.POST["email"]
        # first_name = request.POST["first_name"]
        # last_name = request.POST["last_name"]
        # Check username is already taken
        register_message = ""
        if User.objects.filter(username=username).first():
            register_message =  "This username is already taken"
        # Check the validity of a Password
        elif (len(password) < 8):
            register_message =  "Password must have at least 8"
        elif not re.search("[a-z]", password):
            register_message =  "Password must have at least 1 of a-z"
        elif not re.search("[A-Z]", password):
            register_message =  "Password must have at least 1 of A-Z"
        elif not re.search("[0-9]", password):
            register_message =  "Password must have at least 1 of 0-9"
        # Check re-password is same as password
        elif password != re_password:
            register_message =  "Invalid password confirm"
        # Add Object User
        if register_message == "":
            add_user = User(username=username)
            add_user.set_password(password)
            add_user.save()
            login(request, add_user)
            return render(request, "task/index.html",{'task_list':[],'register_message':'register success'})
        else:
            return render(request, "task/index.html",{'task_list':[],'register_message':register_message})
    return HttpResponseRedirect(reverse("task:index"))



def logout_view(request):
    logout(request)
    return render(request, "task/index.html",{'task_list':[],'logout_message':'logout success'})
