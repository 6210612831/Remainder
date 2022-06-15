import json
from tkinter.messagebox import NO
from rest_framework.generics import  ListCreateAPIView
from task.serializers import TaskSerializer
from task.models import Task
from rest_framework.response import Response
from rest_framework import status  
from datetime import datetime
from django_celery_beat.models import PeriodicTask,IntervalSchedule


# Create your views here.
class TaskListApiView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = TaskSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            
            name=request.data.get('name')
            period_obj = PeriodicTask.objects.create(
                name=name,
                task="task.tasks.line_alert",
                enabled = True,
                start_time=request.data.get('start_time'),
                one_off=True if (request.data.get('repeat').lower())=="false" else False,
                interval = IntervalSchedule.objects.first()
            )
            if request.data.get('every') and request.data.get('period'):
                every = int(request.data.get('every'))
                period = request.data.get('period')
                if len(IntervalSchedule.objects.filter(every = every,period=period))!=0:
                    inter = IntervalSchedule.objects.get(every = every,period=period)
                else:
                    inter = IntervalSchedule.objects.create(
                        every = int(request.data.get('every')),
                        period = request.data.get('period')
                    )
                period_obj.interval = inter
            period_obj.args = '['+"\""+name+"\""+"]"
            period_obj.save()
        
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)