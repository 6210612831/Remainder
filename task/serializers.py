# from .models import Task
from ast import Raise
from functools import cache
import json
from urllib import response
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask as Task
from django_celery_beat.models import IntervalSchedule
from pkg_resources import require
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import requests
from rest_framework import status
from django_celery_beat.models import PeriodicTask


from task.models import Storage

UPLOAD_HOST = "http://127.0.0.1:8000"

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
    # period = serializers.CharField(source='interval.period',required = True)
    period = serializers.ChoiceField(choices = PERIOD_CHOICES)
    start_time = serializers.DateTimeField(required = True)
    one_off = serializers.BooleanField(default=True)
    enabled = serializers.BooleanField(default=True)
    name = serializers.CharField(required = True)
    path = serializers.CharField(required = False)
    file = serializers.FileField(required = False)
    email = serializers.EmailField(required = True)
    file_rename = serializers.CharField(required = False)
    # file_repath = serializers.CharField(required = False)

    
    class Meta:
        model = Task
        exclude = ['task']
        read_only_fields = ('every', 'period')

    def create(self, validated_data):
        # print(validated_data)
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

        storage_id = -1
        try:
            try:
                path = validated_data['path']
                path = path if path[-1] =="/" else path+"/"
            except:
                path = ""
            file = validated_data['file']

            payload = {
                'path':path,
                'file_name':file.name
            }

            with open(file.temporary_file_path(), 'rb') as f:
                response = requests.post(f'{UPLOAD_HOST}/api/v1/upload', data = payload ,files={'file': f})
        except :
            data.delete()
            raise Exception("file error")

        if response.status_code == status.HTTP_201_CREATED:
            storage_id = response.json()['storage_id']
        elif response.status_code == status.HTTP_406_NOT_ACCEPTABLE:
            data.delete()
            raise Exception("This file is alreay exist")
        else:
            data.delete()
            raise Exception("can't upload file because bad request about file")

        data.kwargs= f'{{"task_id": "{str(data.id)}","storage_id": "{str(storage_id)}","email": "{validated_data["email"]}"}}' if  storage_id != -1 else f'{{"task_id": "{str(data.id)}","email": "{validated_data["email"]}"}}'
        data.save()

        return data

    def update(self, instance, validated_data):
        kwargs = json.loads(instance.kwargs)
        storage=Storage.objects.get(id=int(kwargs["storage_id"]))
        # try update file
        try:
            try:
                path = validated_data['path']
                path = path if path[-1] =="/" else path+"/"
            except:
                path = ""
            file = validated_data['file']

            new_payload = {
                'path':path,
                'file_name':file.name,
                'update':True
            }
            old_payload={
                'path': storage.path,
                'update':True
            }

            # Create new file
            with open(file.temporary_file_path(), 'rb') as f:
                response = requests.post(f'{UPLOAD_HOST}/api/v1/upload', data = new_payload ,files={'file': f})
            if response.status_code == status.HTTP_201_CREATED:
                # Delete old file
                requests.delete(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = old_payload)
                # Update data in Storage
                storage.file_name=file.name
                storage.path=path
                storage.save()
            elif response.status_code == status.HTTP_406_NOT_ACCEPTABLE:
                raise Exception("This file is alreay exist")
            else:
                raise Exception("can't upload file because bad request about file")
        except :
            pass
            
        # try rename file ,repath file
        try:
            file_rename = validated_data['file_rename']
            # file_repath = validated_data['file_repath']
            payload={
                'path': storage.path,
                'file_repath':path,
                'file_rename':file_rename,
            }
            old_payload={
                'path': storage.path,
                'update':True
            }
            response = requests.patch(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = payload)
            if response.status_code == status.HTTP_200_OK:
                # Delete old file
                requests.delete(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = old_payload)
                storage.file_name=file_rename
                storage.path=path
                storage.save()
        except:
            pass

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

