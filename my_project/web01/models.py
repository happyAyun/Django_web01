from django.db import models

# Create your models here.

class Content(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=105)
    context = models.CharField(max_length=225)
    # date = models.DateField()   
    cnt = models.IntegerField(default=0)