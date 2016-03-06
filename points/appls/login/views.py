from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from models import BaseUser, Follower
from serializers import UserSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['POST'])
def sign_in(request):
    """
    Sign in by credentials.
    """
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_data = BaseUser.objects.get(user_id=user.id)
            serializer = UserSerializer(user_data)
            return JSONResponse({'user': get_user_data(user)})
        else:
            return JSONResponse({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
        }, status=status.HTTP_401_UNAUTHORIZED)

def user_logout(request):
    logout(request)
    return JSONResponse({})

@api_view(['POST'])
def register(request):
    """
    Register new user.
    """
    data = request.data['user'].copy()
    user = User.objects.create_user(data['username'], data['username'], data['password'])
    user.save()
    extended_user = {'first_name':data['first_name'],
                    'last_name':data['last_name'],
                    'user':user.id}

    serializer = UserSerializer(data=extended_user)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse({'msg':'success', 'user': get_user_data(user)})
    return JSONResponse({'msg':serializer.errors})

@csrf_exempt
@api_view(['POST'])
def get_user(request):
    """
    Get user data.
    """
    user = get_user_data(request.user)
    return JSONResponse({'user': user}, status=201)

@api_view(['POST'])
def edit(request):
    """
    Edit user profile.
    """
    user_data = request.data['user_data']
    user = BaseUser.objects.get(user = request.user.id)
    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.address = user_data['address']
    user.about = user_data['about']
    user.save()
    return JSONResponse({}, status=201)

@api_view(['POST'])
@csrf_exempt
def follow(request):
    """
    Follow by user.
    """
    user_id = request.data['person']
    follower = BaseUser.objects.get(user=request.user.id)
    author = BaseUser.objects.get(user=user_id)
    follower_person = Follower.objects.create(author=author, 
                                              person=follower)
    return JSONResponse({}, status=201)

def get_user_data(user):
    user_data = BaseUser.objects.get(user = user.id)
    return {'id':user.id, 
            'username': user.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'about': user_data.about,
            'address': user_data.address}