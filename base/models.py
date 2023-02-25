from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
    file = models.FileField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    cleared = models.CharField(max_length=200)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title