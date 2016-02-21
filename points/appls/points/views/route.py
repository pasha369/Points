# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from ..models.place import Category, Place, Like, PlacePhoto
from ..models.route import Route, RoutePlace
from ..serializers import CategorySerializer, PlaceSerializer, LikeSerializer

from appls.app.utils.json_response import JSONResponse

from PIL import Image
from django.conf import settings


@csrf_exempt
@api_view(['POST'])
def save_route(request):
    """
    Save route instance after then 
    join place to route
    """
    route = request.data['route']
    author = BaseUser.objects.get(user = request.user.id)
    route_entity = Route.objects.create(name=route['name'],
                                        description=route.get('description'),
                                        author=author)
    route_entity.save()
    for place in route['selectedPlaces']:
        place_entity = Place.objects.get(pk=place['id'])
        route_place_entity = RoutePlace.objects.create(place=place_entity,
                                                       route=route_entity)
        route_place_entity.save()
    return JSONResponse({}, status=201)


@csrf_exempt
@api_view(['POST'])
def get_route_detail(request):
    """
    Get route detail with related places
    """
    route_id = request.data['routeId']
    route_entity = Route.objects.get(pk=route_id)
    route_place_entity = RoutePlace.objects.filter(route__pk=route_id)
    places = []
    for route_place in route_place_entity:
        photo = PlacePhoto.objects.filter(place=route_place.place)
        place = {'id': route_place.place.pk,
                                'title': route_place.place.title,
                                'description': route_place.place.description,
                                'photo': photo[0].photo_url if photo.exists() else "",
                                'latitude': route_place.place.latitude,
                                'langtitude': route_place.place.langtitude,
                                }
        places.append(place)
    route = {'name': route_entity.name,
            'description': route_entity.description,
            'places': places}
    return JSONResponse({'route': route}, status=201)

@csrf_exempt
@api_view(['POST'])
def get_route_list(request):
    """
    Get all routes
    """
    route_entities = Route.objects.all()
    routes = []
    for route in route_entities:
        routes.append({
                     'id': route.pk,
                     'name': route.name,
                     'description': route.description})
    return JSONResponse({'routes': routes}, status=201)
