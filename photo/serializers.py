from rest_framework import serializers
from .models import Photo, Tag, Like, Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    photographer_display_name = serializers.CharField(
        source='photographer.display_name', read_only=True
    )
    image_url = serializers.CharField(
        source='image.url', read_only=True
    )
    tags = TagSerializer(many=True, read_only=True) 

    class Meta:
        model = Photo
        fields = [
            'id', 'photographer', 'photographer_display_name', 'title',
            'description', 'image_url', 'category', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['photographer', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'photographer', 'photo', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    photographer = serializers.ReadOnlyField(source='photographer.user.username')
    photo_title = serializers.ReadOnlyField(source='photo.title')

    class Meta:
        model = Comment
        fields = ['id', 'photographer', 'photo', 'photo_title', 'content', 'created_at', 'updated_at']

