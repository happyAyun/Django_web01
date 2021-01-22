from django.db import models

class User(models.Model):
    objects = models.Manager()
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class Content(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=105)
    context = models.CharField(max_length=225)
    cnt = models.IntegerField(default=0)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

class Reply(models.Model):
    objects = models.Manager()
    user = models.CharField(max_length=50)
    replyCon = models.CharField(max_length=200)
    originalCon = models.ForeignKey(Content, on_delete=models.CASCADE)

    

