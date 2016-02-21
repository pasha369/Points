from rest_framework import serializers 

from models.place import Category, Place, Like
from models.country import Country

from appls.login.models import BaseUser
from appls.login.serializers import UserSerializer
from appls.points.models.place import Place, Category


class CategorySerializer(serializers.Serializer):
    """
    Serializer for category model
    """
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    #places = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for place model
    """
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        model = Place
        fields = ('pk', 'title', 'description', 'author', 'category', 'price',
                  'latitude', 'langtitude', 'address')


    def create(self, validated_data):
        return Place.objects.create(**validated_data)

class LikeSerializer(serializers.Serializer):
    """
    LikeSerializer
    """
    place = serializers.ReadOnlyField(source='place.id')
    user = serializers.ReadOnlyField(source='user.user.username')

    class Meta:
        model = Like
        fields = ('place', 'user')

    def perform_create(self, serializer):
        user = BaseUser.objects.get(user = self.request.user.id)
        serializer.save(user=user)

    def create(self, validated_data):
        return Like.objects.create(**validated_data)
         
class CountrySerializer(serializers.ModelSerializer):
    """
    Country Serializer
    """
    
    class Meta():
        """
        """
        model = Country
        fields = ('id', 'name')
                        