# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^add/$', views.add_comment, name='add'),    
    url(r'^get_by_place/$', views.get_comments_by_place, name='get'),    
]
