from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class BaseUser(models.Model):
    """
    Extended model of standart user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=200, blank=True, default='')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=100, blank=True, default='')
    about = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
        
class Follower(models.Model):
    """Model for follower user"""
    author = models.ForeignKey(BaseUser, default=1, related_name="author")
    person = models.ForeignKey(BaseUser, default=2, related_name="person")
        