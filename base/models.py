import uuid

from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    file = models.FileField(upload_to='uploads/')
    drive_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500)