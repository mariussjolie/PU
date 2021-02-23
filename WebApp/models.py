"""WebApp Models"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Estate(models.Model):
    """Estate Class"""
    address = models.CharField(max_length=60)
    title = models.CharField(max_length=60)
    date = models.DateTimeField(default=timezone.now)
    users = models.ManyToManyField(User)


class Item(models.Model):
    """Item Class"""
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='uploads/images/', default='uploads/images/default_image.png')


class Vote(models.Model):
    """Vote class"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=99)
    importance = models.IntegerField(default=0)
