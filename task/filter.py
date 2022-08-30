import django_filters
# from task.models import Task
from django_celery_beat.models import PeriodicTask
from .models import Task



class PeriodTaskFilter(django_filters.FilterSet):

    id = django_filters.CharFilter(method="filter_by_task_id")
    name = django_filters.CharFilter(field_name="name" , lookup_expr="icontains")
    one_off = django_filters.BooleanFilter(field_name="one_off")
    enabled = django_filters.BooleanFilter(field_name="enabled")

    class Meta:
        model = PeriodicTask
        fields = '__all__'

    def filter_by_task_id(self,queryset,name,value):
        task_ids = value.strip().split(",")
        return queryset.filter(id__in=task_ids)


class TaskFilter(django_filters.FilterSet):

    id = django_filters.CharFilter(method="filter_by_task_id")
    name = django_filters.CharFilter(field_name="name" , lookup_expr="icontains")
    status_todo = django_filters.BooleanFilter(field_name="status_todo")
    status_alert = django_filters.BooleanFilter(field_name="status_alert")

    class Meta:
        model = Task
        fields = '__all__'

    def filter_by_task_id(self,queryset,name,value):
        task_ids = value.strip().split(",")
        return queryset.filter(id__in=task_ids)

# class StorageFilter(django_filters.FilterSet):
#     file_name = django_filters.CharFilter(field_name="file_name" , lookup_expr="icontains")
#     path = django_filters.CharFilter(field_name="path" , lookup_expr="icontains")

#     class Meta:
#         model = Storage
#         fields = '__all__'

