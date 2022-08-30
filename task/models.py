from django.db import models


# class Storage(models.Model):
#     file_name = models.CharField(max_length = 100, blank = False)
#     path = models.CharField(max_length = 200, blank = True)

#     @property
#     def context_data(self):
#         return {
#             'file_name': self.file_name,
#             'path': self.path
#         }
#     def __str__(self):
#         return f"ID : {self.id} , FILE_NAME : {self.file_name} , PATH : {self.path}"


class Task(models.Model):
    name = models.CharField(max_length = 100, blank = False ,unique=True)
    status_todo = models.BooleanField(default=False)
    status_alert = models.BooleanField(default=False)

    @property
    def context_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'status_todo': self.status_todo
        }
    def __str__(self):
        return f"ID : {self.id} , TASK_NAME : {self.name} , STATUS_TODO : {self.status_todo}"

