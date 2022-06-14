from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length = 180, blank = False)
    time = models.DateTimeField(auto_now = False, blank = False)
    repeat = models.BooleanField(max_length=1, blank = False,default=0) # True = repeat alert , False = only alert once
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"ID : {self.id} , TASK : {self.name} , TIME : {self.time} , ACTIVE : {self.active}"