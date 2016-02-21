# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from ..models.place import Category, Place, Like, PlacePhoto
from ..models.country import Country

from ..serializers import CategorySerializer, PlaceSerializer, LikeSerializer, CountrySerializer

from appls.app.utils.json_response import JSONResponse

from PIL import Image
from django.conf import settings

@api_view(['POST'])
@csrf_exempt
def country_list(request):
    """
    Get country list
    """
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return JSONResponse(serializer.data, status=201)