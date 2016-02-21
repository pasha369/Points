# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from models import Comment
from serializers import CommentSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['POST'])
def add_comment(request):
    data = request.data['comment'].copy()
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=404)

@api_view(['POST'])
def get_comments_by_place(request):
    place_id = request.data['place_id']
    comments = Comment.objects.filter(place_id=place_id)
    serializer = CommentSerializer(comments, many=True)
    return JSONResponse(serializer.data, status=201)