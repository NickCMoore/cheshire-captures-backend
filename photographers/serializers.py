from rest_framework import serializers
from .models import Photographer, Follow

class PhotographerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    user = serializers.ReadOnlyField(source='user.username', read_only=True)
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user == obj.user
        return False
    profile_image = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image and obj.profile_image.url.startswith('http'):
            return obj.profile_image.url
        return f'https://res.cloudinary.com/dwgtce0rh/{obj.profile_image.url}'

    def get_cover_image(self, obj):
        if obj.cover_image and obj.cover_image.url.startswith('http'):
            return obj.cover_image.url
        return f'https://res.cloudinary.com/dwgtce0rh/{obj.cover_image.url}'

    class Meta:
        model = Photographer
        fields = [
            'id', 'user', 'display_name', 'bio', 'profile_image', 
            'location', 'cover_image', 'website', 'instagram', 
            'twitter', 'created_at', 'updated_at', 'is_user'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_website(self, value):
        if value and value.strip() and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Website must start with 'http://' or 'https://'.")
        return value

    def validate_instagram(self, value):
        if value and value.strip() and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Instagram link must start with 'http://' or 'https://'.")
        return value

    def validate_twitter(self, value):
        if value and value.strip() and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Twitter link must start with 'http://' or 'https://'.")
        return value

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']
        read_only_fields = ['follower']
