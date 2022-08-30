from django.shortcuts import get_object_or_404
import requests
from rest_framework.views import APIView
from task.serializers import PeriodicTaskSerializer,TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from task.filter import PeriodTaskFilter,TaskFilter
from django_celery_beat.models import PeriodicTask
from rest_framework import permissions
import json
from .models import Task


UPLOAD_HOST = "http://127.0.0.1:8000"


# Create your views here.



class PeriodTaskApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PeriodicTaskSerializer
    queryset = PeriodicTask.objects.all()

    def get(self, request, *args, **kwargs):
        data_set = PeriodicTask.objects.all()
        tasks = PeriodTaskFilter(request.GET,queryset=data_set).qs

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
            return Response(task.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(task.errors, status=status.HTTP_401_UNAUTHORIZED)
        


class PeriodTaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = PeriodicTaskSerializer
    queryset = PeriodicTask.objects.all()

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(PeriodicTask, pk=kwargs['pk'])
        kwargs = json.loads(task.kwargs)
        # storage=Storage.objects.get(id=int(kwargs["storage_id"]))
        # payload={
        #     'path': storage.path
        # }
        # response = requests.get(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = payload)

        data = {
            'name':task.name,
            'task':task.task,
            'kwargs':task.kwargs,
            'one_off':task.one_off,
            'enabled':task.enabled,
            'start_time':task.start_time,
            # 'download_url':response.json(),
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
        # storage=Storage.objects.get(id=int(kwargs["storage_id"]))
        # payload={
        #     'path': storage.path
        # }
        # response = requests.delete(f'{UPLOAD_HOST}/api/v1/upload/{storage.file_name}', data = payload)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        context = task.__str__()
            # check if no other periodtask using this interval then delete it too
        interval_using_by_period = PeriodicTask.objects.filter(interval = task.interval)
        if len(interval_using_by_period) == 1:
            task.interval.delete()
        task.delete()
            # storage.delete()
        return Response(context, status=status.HTTP_204_NO_CONTENT)


class TaskApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        data_set = Task.objects.all()
        tasks = TaskFilter(request.GET,queryset=data_set).qs
        
        task_context_list=[]
        for task in tasks:
            # task_context_list.append(task.__str__())
            task_context_list.append(task.context_data)
        print(task_context_list)
        return Response(task_context_list, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        task = TaskSerializer(data = request.data)
        if task.is_valid():
            task.save()
            return Response(task.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        kwargs = json.loads(task.kwargs)
        data = {
            'name':task.name,
            'status_todo':task.status_todo,
            'status_alert':task.status_alert,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            task = serializer.save()
        return Response(task.__str__(), status=200)

    def delete(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        context = task.__str__()
        task.delete()
        return Response(context, status=status.HTTP_204_NO_CONTENT)