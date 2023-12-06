from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class File(models.Model):

#     name = models.CharField(max_length=200)
#     size = models.BigIntegerField()
#     path = models.CharField(max_length=200)

class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')