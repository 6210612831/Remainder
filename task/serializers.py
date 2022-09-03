# from .models import Task
from ast import Raise
from dataclasses import field
from functools import cache
import json
from urllib import response
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask as Task
from .models import Task as TaskModel
from django_celery_beat.models import IntervalSchedule
from pkg_resources import require
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import requests
from rest_framework import status
from django_celery_beat.models import PeriodicTask
from django.contrib.auth.models import User


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



class PeriodicTaskSerializer(serializers.ModelSerializer):
    DAYS = DAYS
    HOURS = HOURS
    MINUTES = MINUTES
    SECONDS = SECONDS
    MICROSECONDS = MICROSECONDS

    PERIOD_CHOICES = PERIOD_CHOICES


    every = serializers.IntegerField(required = True)
    period = serializers.ChoiceField(choices = PERIOD_CHOICES)
    start_time = serializers.DateTimeField(required = True)
    one_off = serializers.BooleanField(default=True)
    enabled = serializers.BooleanField(default=True)
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)


    
    class Meta:
        model = Task
        exclude = ['task']
        read_only_fields = ('every', 'period')

    def create(self, validated_data):
        interval_obj = ''
        if len(IntervalSchedule.objects.filter(every = int(validated_data['every']),period = validated_data['period'])) == 0:
            interval_obj = IntervalSchedule.objects.create(
                every = int(validated_data['every']),
                period = validated_data['period']
            )
        else:
            interval_obj = IntervalSchedule.objects.filter(every = int(validated_data['every']),period = validated_data['period']).first()

        data=Task.objects.create(
            name=validated_data['name'],
            task="task.tasks.send_email",
            enabled=validated_data['enabled'],
            start_time=validated_data['start_time'],
            one_off=validated_data['one_off'],
            interval=interval_obj,
        )

        data.kwargs= f'{{"task_id": "{str(data.id)}","email": "{validated_data["email"]}"}}'
        data.save()

        return data

    def update(self, instance, validated_data):
        kwargs = json.loads(instance.kwargs)

        interval = instance.interval

        # * PeriodicTask Info
        instance.name = validated_data.get(
            'name', instance.name)
        instance.last_name = validated_data.get(
            'enabled', instance.enabled)
        instance.one_off = validated_data.get(
            'one_off', instance.one_off)
        instance.start_time = validated_data.get(
            'start_time', instance.start_time)
        instance.save()

        # check if no other periodtask using this interval then change value but if in use by other peroid then create new one
        interval_using_by_period = Task.objects.filter(interval = instance.interval)
        if len(interval_using_by_period) == 1:
            interval.every = int(validated_data.get(
                'every', interval.every))
            interval.period = validated_data.get(
                'period', interval.period)
            interval.save()
        else:
            interval_obj = IntervalSchedule.objects.create(
                every = int(validated_data.get('every',instance.interval.every)),
                period = validated_data.get('period',instance.interval.period)
            )
            instance.interval = interval_obj
            instance.save()

        return instance





class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required = True)
    user_id = serializers.CharField(required = True)
    class Meta:
        model = TaskModel
        # fields = "__all__"
        exclude = ['owner']
        read_only_fields = ('user_id',)

    def create(self, validated_data):
        user_id=validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        instance=TaskModel.objects.create(name=validated_data['name'],owner=user)
        return instance

    @property
    def context_data(self):
        user=User.objects.get(id=self.user_id)
        return {
            'name': self.name,
            'owner': user.username
        }