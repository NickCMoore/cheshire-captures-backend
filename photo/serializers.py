from rest_framework import serializers
from .models import Photo, Tag, Like, Comment

class PhotoSerializer(serializers.ModelSerializer):
    photographer_display_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    def get_photographer_display_name(self, obj):
        return obj.photographer.display_name or obj.photographer.user.username

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    class Meta:
        model = Photo
        fields = [
            'id', 'photographer', 'photographer_display_name', 'title',
            'description', 'image_url', 'category', 'tags', 'created_at', 'updated_at'
        ]
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
