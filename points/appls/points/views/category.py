# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from ..models.place import Category, Place, PlacePhoto
from ..serializers import CategorySerializer, PlaceSerializer
from appls.app.utils.json_response import JSONResponse


@api_view(['POST'])
@csrf_exempt
def categort_list(request):
    """
    Get category list
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return JSONResponse(serializer.data, status=201)

@api_view(['POST'])
@csrf_exempt
def get_category_places(request):
    """
    Get place by selected category
    """
    category_id = request.data['category_id']
    places = Place.objects.filter(category=category_id)
    place_data = get_place_data(places)
    return JSONResponse({'places': place_data}, status=201)

def get_place_data(places):
    place_data = []
    first = 0
    for place in places:
        photo = PlacePhoto.objects.filter(place=place)
        place_data.append({
            'user': place.author.user.username if place.author is not None else "",
            'title': place.title,
            'description': place.description,
            'id': place.id,
            'category': place.category.name  if place.category is not None else "",
            'photo': photo[first].photo_url if photo.exists() else ""
        })
    return place_data