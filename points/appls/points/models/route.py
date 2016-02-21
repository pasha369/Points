# -*- coding: utf-8 -*-
from django.db import models
from appls.login.models import BaseUser
from appls.points.models.place import Place


class Route(models.Model):
    """
    Model for route
    """
    name = models.CharField(max_length=60, blank=False, default='_')
    description = models.TextField(blank=True, default='')
    author = models.ForeignKey(BaseUser, blank=True, null=True, on_delete=models.SET_NULL)

class RoutePlace(models.Model):
    """
    Model for join route and related places.
    """
    route = models.ForeignKey(Route, blank=True, null=True, on_delete=models.SET_NULL) 
    place = models.ForeignKey(Place, blank=True, null=True, on_delete=models.SET_NULL) 