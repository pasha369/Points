from __future__ import unicode_literals

from django.db import models
from appls.login.models import BaseUser
from appls.points.models.place import Place

class Comment(models.Model):
    """
    Model for comment.
    """
    text = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(BaseUser, default=1)
    place = models.ForeignKey(Place, default=1)
    created = models.DateTimeField(auto_now_add=True)