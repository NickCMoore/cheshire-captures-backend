from rest_framework import serializers
from .models import Photo, Tag, Like, Comment, PhotoRating

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name'] 

class PhotoRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  

    class Meta:
        model = PhotoRating
        fields = ['id', 'user', 'photo', 'rating', 'created_at']

class PhotoSerializer(serializers.ModelSerializer):
    photographer = serializers.ReadOnlyField(source='photographer.username')  
    image_url = serializers.CharField(source='image.url', read_only=True)  
    tags = TagSerializer(many=True, read_only=True) 
    average_rating = serializers.DecimalField(source='rating', max_digits=3, decimal_places=2, read_only=True)
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            'id', 'photographer', 'title', 'description', 'image_url',
            'category', 'tags', 'created_at', 'updated_at',
            'average_rating', 'user_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = PhotoRating.objects.filter(photo=obj, user=request.user).first()
            return rating.rating if rating else None
        return None

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Like
        fields = ['id', 'photo', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  
    photo = serializers.PrimaryKeyRelatedField(queryset=Photo.objects.all())  
    class Meta:
        model = Comment
        fields = ['id', 'photo', 'user', 'content', 'created_at', 'updated_at'] 

    def create(self, validated_data):
        user = self.context['request'].user
        photo = validated_data['photo'] 
        content = validated_data['content'] 
        
        return Comment.objects.create(user=user, photo=photo, content=content)
