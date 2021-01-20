from django.db import models

# Create your models here.

class Content(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=105)
    context = models.CharField(max_length=225)
    cnt = models.IntegerField(default=0)

class User(models.Model):
    objects = models.Manager()
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
