# -*- coding: utf-8 -*-
from django.db import models
from appls.login.models import BaseUser
from appls.points.models.country import Country, City


class Place(models.Model):
    """
    Model for place
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    country = models.ForeignKey('Country', blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=120, blank=True, default='')
    latitude = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    langtitude = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=4, default=0, null=True)

    author = models.ForeignKey(BaseUser, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created',)

class PlacePhoto(models.Model):
    """
    Model for place photo
    """
    place = models.ForeignKey('Place', blank=True, null=True, on_delete=models.SET_NULL)
    photo_url = models.CharField(max_length=200, blank=True, default='')

class Like(models.Model):
    """
    Model for like
    """
    user = models.ForeignKey(BaseUser, default=1)
    place = models.ForeignKey(Place, default=1)

class Category(models.Model):
    """
    Model for category
    """
    name = models.CharField(max_length=100, blank=False, default='default category')
    
    class Meta:
        ordering = ('name',)