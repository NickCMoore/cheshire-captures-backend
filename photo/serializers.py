from rest_framework import serializers
from .models import Photo, Tag, Like

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photographer', 'title', 'description', 'image', 'category', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['photographer', 'created_at', 'updated_at']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'photographer', 'photo', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    photographer = serializers.ReadOnlyField(source='photographer.user.username')

    class Meta:
        model = Comment
        fields = ['id', 'photographer', 'photo', 'content', 'created_at', 'updated_at']
