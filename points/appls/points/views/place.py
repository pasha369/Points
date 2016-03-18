# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from appls.login.models import BaseUser
from ..models.place import Category, Place, Like, PlacePhoto
from ..serializers import CategorySerializer, PlaceSerializer, LikeSerializer

from appls.app.utils.json_response import JSONResponse

from PIL import Image
from django.conf import settings


@api_view(['GET'])
@csrf_exempt
def place_list(request):
    """
    Get place list.
    """
    places = Place.objects.all()
    place_data = get_place_data(places)
    return JSONResponse({'places': place_data}, status=201)


@api_view(['POST'])
@csrf_exempt
def add_place(request):
    """
    Add new place to db.
    """
    if request.method == 'POST':
        data = request.data['place'].copy()
        data['author'] = BaseUser.objects.get(user = request.user).id
        data['price'] = 2.2
        photo = request.data['place']['photo']

        serializer = PlaceSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            place_id = serializer.data['pk']
            place = Place.objects.get(pk=place_id)
            photo_place = PlacePhoto.objects.create(place=place, photo_url=photo)
            photo_place.save()
            return JSONResponse({'place': serializer.data
                                ,'photo': photo_place.photo_url}
                                , status=201)
        return JSONResponse(serializer.errors, status=404)

@api_view(['POST'])
@csrf_exempt
def remove_place(request):
    """
    Delete place from db.
    """
    id = request.data['place_id']
    place = Place.objects.get(pk=id)
    place.delete()
    return JSONResponse({}, status=201)


@api_view(['POST'])
@csrf_exempt
def get_place_detail(request):
    """
    Get place detail by id.
    """
    id = request.data['place_id']
    place = Place.objects.get(pk=id)
    photo = PlacePhoto.objects.filter(place=place)
    place_data = ({
        'user': place.author.user.username if place.author is not None else "",
        'title': place.title,
        'description': place.description,
        'id': place.id,
        'latitude': place.latitude,
        'langtitude': place.langtitude,
        'category': place.category.name  if place.category is not None else "",
        'photo': photo[0].photo_url if photo.exists() else ""
    })
    return JSONResponse(place_data, status=201)

@api_view(['POST'])
@csrf_exempt
def get_by_user(request):
    author = BaseUser.objects.get(user = request.user.id)
    places = Place.objects.filter(author__id=author.id)
    place_data = get_place_data(places)
    serializer = PlaceSerializer(places, many=True)
    return JSONResponse({'places': place_data}, status=201)

@api_view(['POST'])
@csrf_exempt
def get_place_page(request):
    page_id = request.data['page_id']
    places = get_page(page_id, Place.objects.all())
    serializer = PlaceSerializer(places, many=True)
    return JSONResponse(serializer.data, status=201)


@api_view(['POST'])
@csrf_exempt
def search(request):
    """
    Search place by entered title.
    """
    search_text = request.data['search_text']
    search_data = Place.objects.filter(title__icontains=search_text.lower())
    places = get_place_data(search_data)
    return JSONResponse({'places': places}, status=201)

@api_view(['POST'])
@csrf_exempt
def get_place_by_id(request):
    # TODO: implement get place by index
    pass

def get_page(page_id, places):
    item_on_page = 5
    if page_id != None and page_id != 0:
        item_first_id = (page_id-1)*item_on_page
        item_last_id= page_id*item_on_page
        places = places[item_first_id: item_last_id]
    else:
        places = places[page_id: item_on_page]
    return places

@api_view(['POST'])
@csrf_exempt
def place_like(request):
    """
    Like place.
    """
    place_id = request.data['place']
    place = Place.objects.get(pk=place_id)
    user = BaseUser.objects.get(user = request.user.id)
    Like.objects.create(place=place, user=user)
    return JSONResponse({}, status=201)

@api_view(['POST'])
@csrf_exempt
def get_place_likes(request):
    """
    Get place like count.
    """
    place_id = request.data['place_id']
    like_count = Like.objects.filter(place=place_id).count()
    return JSONResponse({'like_count': like_count}, status=201)

@api_view(['POST'])
@csrf_exempt
def save_place_photo(request):
    """
    Bind photo to place.
    """
    photo = request.FILES['photo']
    path = 'media/' + photo.name
    with Image.open(photo) as pil_image:
                # Check format of input image
        if pil_image.format not in ('GIF', 'JPEG', 'PNG'):
            raise Exception("Unsupport image type. Please upload bmp, png or jpeg")
        pil_image.save(path) 
    return JSONResponse({'path': path}, status=201)


def get_place_data(places):
    """
    Get place data.
    """
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