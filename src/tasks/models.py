from django.db import models
from django.conf import settings

# Create your models here.


class TaskQuerySet(models.QuerySet):
    pass


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    task = models.TextField()
    is_completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TaskManager()

    def __str__(self):
        return str(self.task)[:50]

    @property
    def owner(self):
        return self.user
