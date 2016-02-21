# -*- coding: utf-8 -*-
from django.db import models
from appls.login.models import BaseUser


class Country(models.Model):
    """
    Model for Country
    """
    name = models.CharField(max_length=100, blank=False, default='default category')
    
    class Meta:
        ordering = ('name',)

class City(models.Model):
    """
    Model for City
    """
    country = models.ForeignKey('Category', default=1)
    name = models.CharField(max_length=100, blank=False, default='default category')
    
    class Meta:
        ordering = ('name',)


        

