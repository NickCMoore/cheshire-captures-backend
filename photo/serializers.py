from rest_framework import serializers
from .models import Photo, Tag, Like, Comment, PhotoRating  

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PhotoRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = PhotoRating
        fields = ['id', 'user', 'photo', 'rating', 'created_at']

class PhotoSerializer(serializers.ModelSerializer):
    photographer_display_name = serializers.CharField(
        source='photographer.display_name', read_only=True
    )
    image_url = serializers.CharField(
        source='image.url', read_only=True
    )
    tags = TagSerializer(many=True, read_only=True) 
    average_rating = serializers.DecimalField(
        source='rating', max_digits=3, decimal_places=2, read_only=True
    )
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            'id', 'photographer_display_name', 'title',
            'description', 'image_url', 'category', 'tags', 'created_at', 
            'updated_at', 'average_rating', 'user_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = PhotoRating.objects.filter(photo=obj, user=request.user).first()
            return rating.rating if rating else None
        return None

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
