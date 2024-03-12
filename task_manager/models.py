from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, null=True, related_name="workers"
    )

    class Meta:
        ordering = [
            "position",
            "username",
        ]

    def __str__(self):
        return f"{self.position} | {self.username}: {self.first_name} {self.last_name}"


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    class PriorityStatus(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"
        IMPORTANT = "important", "Important"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=63, choices=PriorityStatus, default=PriorityStatus.LOW
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = [
            "is_completed",
            "priority",
            "deadline",
        ]

    def __str__(self):
        return f"{self.name} ({self.priority}) | {'Completed' if self.is_completed else ('Deadline: ',  self.deadline)}"
