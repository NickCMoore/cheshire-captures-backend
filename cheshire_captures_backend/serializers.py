from dj_rest_auth.serializers import UserDetailsSerializer, TokenSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    photographer_id = serializers.ReadOnlyField(source='photographer.id')
    profile_image = serializers.ReadOnlyField(
        source='photographer.profile_image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'photographer_id', 'profile_image'
        )


class CustomTokenSerializer(TokenSerializer):
    user = CurrentUserSerializer(many=False, read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + (
            'user',
        )
