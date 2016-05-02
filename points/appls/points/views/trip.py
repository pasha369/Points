from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from ..models.place import Category, Place
from ..models.route import Route
from ..models.trip import Trip, TripFollower

from appls.app.utils.json_response import JSONResponse


@csrf_exempt
@api_view(['POST'])
def create_trip(request):
    """
    Create new trip.
    """
    route = Route.objects.get(pk=request.data['routeId'])
    author = BaseUser.objects.get(user = request.user.id)
    trip_entity = Trip.objects.create(route=route, 
                                      author=author,
                                      date_from=request.data['dateFrom'],
                                      date_to=request.data['dateTo'])
    trip_entity.save()
    _subscribe(request.user.id, trip_entity)
    return JSONResponse({}, status=201)

@csrf_exempt
@api_view(['POST'])
def get_all(request):
    """
    Get all trip.
    """
    trips = _convert_to_json(Trip.objects.all())
    return JSONResponse({'trips': trips}, status=201)

@csrf_exempt
@api_view(['POST'])
def subscribe_trip(request):
    """
    Subscribe on trip.
    """
    trip = Trip.objects.get(pk=request.data['tripId'])
    _subscribe(request.user.id, trip)
    return JSONResponse({}, status=201)

@csrf_exempt
@api_view(['POST'])
def discard_trip(request):
    """
    Discard from trip.
    """
    trip = Trip.objects.get(pk=request.data['tripId'])
    subsciber = BaseUser.objects.get(user = request.user.id)
    trip_follower = TripFollower.objects.filter(trip=trip, follower=subsciber)
    followers_count = TripFollower.objects.filter(trip=trip).count()
    if followers_count <= 1:
        trip_follower[0].delete()
        trip.delete()
    else:
        trip_follower[0].delete()
    return JSONResponse({}, status=201)

@csrf_exempt
@api_view(['POST'])
def get_trip_by_user(request):
    """
    Get trips by user.
    """
    subsciber = BaseUser.objects.get(user = request.user.id)
    trip_enties = [x.trip for x in TripFollower.objects.filter(follower=subsciber)]
    trips = _convert_to_json(trip_enties)
    return JSONResponse({'trips': trips}, status=201)

@csrf_exempt
@api_view(['POST'])
def get_trip_date(request):
    """
    Get trip date list.
    """
    trips = []
    trip_entities = TripFollower.objects.filter(trip__route__pk=request.data['tripId'])
    print request.data['tripId']
    for trip in trip_entities:
        people_count = TripFollower.objects.filter(trip__pk=trip.trip.pk).count()
        trips.append({'tripId': trip.trip.pk,
                     'dateFrom': trip.trip.date_from.strftime('%Y-%m-%d'),
                     'dateTo': trip.trip.date_to.strftime('%Y-%m-%d'),
                     'peopleCount': people_count})
    return JSONResponse({'trips': trips}, status=201)

def _subscribe(userId, trip):
    """
    subscribe on trip.
    """
    subsciber = BaseUser.objects.get(user = userId)
    trip_follower = TripFollower.objects.create(trip=trip, 
                                                follower=subsciber)
    trip_follower.save()

def _convert_to_json(trip_entities):
    """
    Convert to json representation
    """
    trips = []
    for trip in trip_entities:
        people_count = TripFollower.objects.filter(trip=trip).count()
        trips.append({'tripId': trip.pk,
                     'route': trip.route.name,
                     'dateFrom': trip.date_from.strftime('%Y-%m-%d'),
                     'dateTo': trip.date_to.strftime('%Y-%m-%d'),
                     'peopleCount': people_count})
    return trips