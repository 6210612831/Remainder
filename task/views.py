from calendar import month
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from task.serializers import TaskSerializer
from task.models import Task
from rest_framework.response import Response
from rest_framework import status  
from datetime import datetime


# Create your views here.
class TaskListApiView(ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # day =request.data.get('day')
        # month = request.data.get('month')
        # year =  request.data.get('year')
        # hour = request.data.get('hour')
        # minute = request.data.get('minute')
        # try:
        #     if not (0<int(day)<=30):
        #         raise Exception
        #     if not (0<int(month)<=12):
        #         raise Exception
        #     if not (0<int(year[2:])<=99):
        #         raise Exception
        #     if not (0<=int(hour)<=23):
        #         raise Exception
        #     if not (0<=int(minute)<=59):
        #         raise Exception   
        # except:
        #     return Response({"ERROR" : "Your alert time is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    

        # check_date_time_str = f"{day}/{month}/{year[2:]} {hour}:{minute}:00"
        # # CHECK DATE IS VALID (example -> 29/2/2022 is not real)
        # try: 
        #     datetime.strptime(check_date_time_str, '%d/%m/%y %H:%M:%S')
        # except:
        #     return Response({"ERROR" : "Your input date cant be real"}, status=status.HTTP_400_BAD_REQUEST)
        # check_date_time_obj = datetime.strptime(check_date_time_str, '%d/%m/%y %H:%M:%S')
        # # CHECK INPUT TIME IS OLDER THAN NOW?
        # if check_date_time_obj < datetime.now():
        #     return Response({"ERROR" : "Your alert time is older than now"}, status=status.HTTP_400_BAD_REQUEST)


        # date_time_str = f"{day}/{month}/{year[2:]} {hour}:{minute}:00++0700"
        # # CHECK DATE IS VALID (example -> 29/2/2022 is not real)
        # try: 
        #     datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S+%z')
        # except:
        #     return Response({"ERROR" : "Your input date cant be real"}, status=status.HTTP_400_BAD_REQUEST)
        # date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S+%z')

        # # INSERT INPUT TO SERIALIZER
        # data = {
        #     "name":request.data.get('name'),
        #     "time":date_time_obj,
        #     "repeat":True if (request.data.get('repeat')).lower()=="yes" else False,
        # }
        serializer = TaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)