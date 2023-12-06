from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def image_url(self):
       return self.image.url