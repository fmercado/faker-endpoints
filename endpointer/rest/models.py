from django.db import models

# Create your models here.

class Cache(models.Model):
    url = models.CharField(max_length=200)
    response_text = models.CharField(max_length=2000)