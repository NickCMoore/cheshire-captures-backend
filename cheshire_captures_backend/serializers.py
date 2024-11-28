from dj_rest_auth.serializers import UserDetailsSerializer, TokenSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serializer for the current authenticated user.
    Includes additional fields for the photographer profile.
    """
    photographer_id = serializers.ReadOnlyField(source='photographer.id')
    profile_image = serializers.ReadOnlyField(
        source='photographer.profile_image.url'
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'photographer_id',
            'profile_image',
        )


class CustomTokenSerializer(TokenSerializer):
    """
    Custom serializer for token authentication.
    Includes the serialized user details within the token response.
    """
    user = CurrentUserSerializer(many=False, read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + (
            'user',
        )
