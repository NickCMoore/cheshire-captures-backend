from rest_framework import serializers
from .models import Photo, Tag

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photographer', 'title', 'description', 'image', 'category', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['photographer', 'created_at', 'updated_at']
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
