# -*- coding: utf-8 -*-
from django.db import models
from appls.login.models import BaseUser
from ..models.route import Route


class Trip(models.Model):
    """
    Trip model.
    """
    route = models.ForeignKey(Route, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(BaseUser, blank=True, null=True, on_delete=models.SET_NULL)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

class TripFollower(models.Model):
    """
    TripFollower model.
    """
    trip = models.ForeignKey(Trip, blank=True, null=True, on_delete=models.SET_NULL)
    follower = models.ForeignKey(BaseUser, blank=True, null=True, on_delete=models.SET_NULL)