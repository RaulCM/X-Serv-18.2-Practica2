from django.db import models

# Create your models here.


class Urls(models.Model):
    url_larga = models.CharField(max_length=64)
