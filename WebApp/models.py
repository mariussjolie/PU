from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Estate = Dødsbo
class Estate(models.Model):
    address = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    date = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(User)


class Item(models.Model):
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
