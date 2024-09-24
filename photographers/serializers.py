from rest_framework import serializers
from .models import Photographer

class PhotographerSerializer(serializers.ModelSerializer):
    # Custom fields for formatted dates
    created_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d %b %Y", read_only=True)
    user = serializers.ReadOnlyField(source='user.username')  # Display the username of the photographer

    class Meta:
        model = Photographer
        fields = [
            'id', 'user', 'display_name', 'bio', 'profile_image', 
            'location', 'cover_image', 'website', 'instagram', 
            'twitter', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_website(self, value):
        """Ensure the website field contains a valid URL."""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Website must start with 'http://' or 'https://'.")
        return value

    def validate_instagram(self, value):
        """Ensure the Instagram field contains a valid URL."""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Instagram link must start with 'http://' or 'https://'.")
        return value

    def validate_twitter(self, value):
        """Ensure the Twitter field contains a valid URL."""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Twitter link must start with 'http://' or 'https://'.")
        return value
