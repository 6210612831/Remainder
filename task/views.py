from django.shortcuts import get_object_or_404
import requests
from rest_framework.views import APIView
from task.serializers import PeriodicTaskSerializer
from rest_framework.response import Response
from rest_framework import status
from task.filter import TaskFilter,StorageFilter
from django_celery_beat.models import PeriodicTask
from rest_framework import permissions
import json
import boto3
# from io import BytesIO
# from PIL import Image
# import os
# import sys
# import threading

from .models import Storage


ACCESS_KEY = "-"
SECRET_KEY = "-"

AWS_ACCOUNT_ID = "-"
BUCKET = "-"

UPLOAD_HOST = "http://127.0.0.1:8000"


# Create your views here.



class TaskApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PeriodicTaskSerializer
    queryset = PeriodicTask.objects.all()

    def get(self, request, *args, **kwargs):
        data_set = PeriodicTask.objects.all()
        tasks = TaskFilter(request.GET,queryset=data_set).qs

        task_context_list=[]
        for task in tasks:
            task_context_list.append(task.__str__())

        return Response(task_context_list, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        task = PeriodicTaskSerializer(data = request.data)
        if task.is_valid():
            try:
                task.save()
            except Exception as ex:
                return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
            try:
                file=task.validated_data.pop('file')
                task.validated_data.update({'file':file.name})
            except:
                pass
            return Response(task.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(task.errors, status=status.HTTP_401_UNAUTHORIZED)
        


class TaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PeriodicTaskSerializer
    queryset = PeriodicTask.objects.all()

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(PeriodicTask, pk=kwargs['pk'])
        kwargs = json.loads(task.kwargs)
        storage=Storage.objects.get(id=int(kwargs["storage_id"]))
        payload={
            'path': storage.path
        }
        response = requests.get(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = payload)

        data = {
            'name':task.name,
            'task':task.task,
            'kwargs':task.kwargs,
            'one_off':task.one_off,
            'enabled':task.enabled,
            'start_time':task.start_time,
            'download_url':response.json(),
        }
        return Response(data, status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        task = get_object_or_404(PeriodicTask, pk=kwargs['pk'])
        serializer = PeriodicTaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
        return Response(task.__str__(), status=200)

    def delete(self, request, *args, **kwargs):
        task = get_object_or_404(PeriodicTask, pk=kwargs['pk'])
        kwargs = json.loads(task.kwargs)
        storage=Storage.objects.get(id=int(kwargs["storage_id"]))
        payload={
            'path': storage.path
        }
        response = requests.delete(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = payload)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            context = task.__str__()
            # check if no other periodtask using this interval then delete it too
            interval_using_by_period = PeriodicTask.objects.filter(interval = task.interval)
            if len(interval_using_by_period) == 1:
                task.interval.delete()
            task.delete()
            storage.delete()
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)



class UploadApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # ==========================  Get file path information ========================== 
        data_set = Storage.objects.all()
        storages = StorageFilter(request.GET,queryset=data_set).qs

        storage_context_list=[]
        for storage in storages:
            storage_context_list.append(storage.__str__())
            
        return Response(storage_context_list, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        # ==========================  Upload file ==========================
        try:
            try:
                update = request.data['update']
            except:
                update = False
            try:
                path = request.data['path']
                path = path if path[-1] =="/" else path+"/"
            except:
                path = ""
            try:
                filename = request.data['file_name']
            except:
                filename = request.data['file'].name

            filepath = request.data['file'].temporary_file_path()
            
            if len(Storage.objects.filter(file_name=filename,path = path)) != 0:
                return Response("This file is alreay exist", status=status.HTTP_406_NOT_ACCEPTABLE)
            
            client = boto3.client( 
                's3',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,)
            client.upload_file(filepath, BUCKET, path+filename)

            # Store path and filename in server database
            if not update:
                obj = Storage.objects.create(file_name=filename,path = path)
                return Response({'storage_id':obj.id}, status=status.HTTP_201_CREATED)
            return Response("Done!", status=status.HTTP_201_CREATED)
        except:
            return Response("BAD_REQUEST", status=status.HTTP_400_BAD_REQUEST)



class UploadDetailApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = []

    def get(self, request, *args, **kwargs):
        # ==========================  Download file ========================== 
        try:
            try:
                path = request.data['path']
                path = path if path[-1] =="/" else path+"/"
            except:
                path = ""
            file_path = path+kwargs['filename']
            Storage.objects.get(file_name=kwargs['filename'],path = path)
            client = boto3.client( 
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,)

            param = {
                    'Bucket' : BUCKET,
                    'Key' : file_path,
                    'ExpectedBucketOwner' : AWS_ACCOUNT_ID
            }

            response = client.generate_presigned_url("get_object",param)
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response("You have to assign filename and path correctly", status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, *args, **kwargs):
        # ==========================  RENAME,REPATH file ========================== 
        try:
            try:
                old_path = request.data['path']
                old_path = old_path if old_path[-1] =="/" else old_path+"/"
            except:
                old_path = ""
            try:
                new_path = request.data['file_repath']
                new_path = new_path if new_path[-1] =="/" else new_path+"/"
            except:
                new_path = ""
            old_file_path = old_path+kwargs['filename']
            new_file_path = new_path+request.data['file_rename']
            Storage.objects.get(file_name=kwargs['filename'],path = old_path)
            client = boto3.client( 
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,)

            copy_source = {
                'Bucket': BUCKET,
                'Key': old_file_path
            }
            client.copy(copy_source, BUCKET, new_file_path)

            return Response("Done!", status=status.HTTP_200_OK)
        except:
            return Response("You have to assign filename and path correctly", status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, *args, **kwargs):
        # ==========================  Delete file ========================== 
        try:
            try:
                path = request.data['path']
                path = path if path[-1] =="/" else path+"/"
            except:
                path = ""
            try:
                update = request.data['update']
            except:
                update = False
            file_path = path+kwargs['filename']
            
            client = boto3.client( 
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,)
        
            response = client.delete_object(
                Bucket=BUCKET,
                Key=file_path,
                ExpectedBucketOwner= AWS_ACCOUNT_ID
            )
            if not update:
                obj = Storage.objects.get(file_name=kwargs['filename'],path = path)
                obj.delete()

            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response("You have to assign filename and path correctly", status=status.HTTP_404_NOT_FOUND)
