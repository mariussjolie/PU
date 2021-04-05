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
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Item(models.Model):
    """Item Class"""
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='uploads/images/', default='uploads/images/default_image.png')
    has_everyone_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Vote(models.Model):
    """Vote class"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.CharField(max_length=99)
    importance = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'item'], name="unique_useritem")
        ]


class Notify(models.Model):
    """Class for notifying user to finish estate"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'estate'], name="unique_notification")
        ]

class Comment(models.Model):
    """Class for comments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
