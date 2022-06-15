from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'
MICROSECONDS = 'microseconds'


PERIOD_CHOICES = (
    (DAYS, _('Days')),
    (HOURS, _('Hours')),
    (MINUTES, _('Minutes')),
    (SECONDS, _('Seconds')),
    (MICROSECONDS, _('Microseconds')),
)

class Task(models.Model):
    name = models.CharField(max_length=200, unique=True)
    #task = models.CharField(max_length=200)
    repeat = models.BooleanField(max_length=1, blank = False,default=0)
    start_time = models.DateTimeField(auto_now = False, blank = False)
    every = models.IntegerField(
        null=True,
        validators=[MinValueValidator(1)],
        blank=True
    )
    period = models.CharField(
        max_length=24, 
        choices=PERIOD_CHOICES,
        null=True,
        blank=True
    )
    active = models.BooleanField(default=True)
    #id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"ID : {self.id} , TASK : {self.name} , TIME : {self.start_time} , ACTIVE : {self.active}"