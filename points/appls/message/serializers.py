from rest_framework import serializers 

from models import Comment
from appls.login.models import BaseUser
from appls.points.models.place import Place


class CommentSerializer(serializers.ModelSerializer):
    """
    docstring for CommentSerializer
    """
    text = serializers.CharField(required=True)
    author = serializers.ReadOnlyField(source='author.user.username')

    class Meta:
        """docstring for Meta"""
        model = Comment
        fields = ('id', 'text', 'author', 'place')
            
    def perform_serializer(self, serializer):
        author = BaseUser.objects.get(user = self.request.user.id)
        serializer.save(author=author)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
        