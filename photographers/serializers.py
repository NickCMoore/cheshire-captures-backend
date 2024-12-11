from rest_framework import serializers
from .models import Photographer, Follow

class PhotographerSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    user = serializers.ReadOnlyField(source='user.username', read_only=True)
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        # Get the request object from the serializer context
        request = self.context.get('request', None)
        if request:
            if request.user.is_authenticated:
                is_current_user = request.user == obj.user
                print(f"DEBUG: Request User: {request.user}, Photographer User: {obj.user}, is_user: {is_current_user}")
                return is_current_user
            else:
                print("DEBUG: User not authenticated.")
        else:
            print("DEBUG: Request context missing.")
        return False

    class Meta:
        model = Photographer
        fields = [
            'id', 'user', 'display_name', 'bio', 'profile_image',
            'location', 'cover_image', 'website', 'instagram',
            'twitter', 'created_at', 'updated_at', 'is_user'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    # Validation methods for URLs
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