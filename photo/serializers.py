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
    average_rating = serializers.DecimalField(
        source='rating', max_digits=3, decimal_places=2, read_only=True
    )
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = [
            'id', 'photographer', 'title', 'description', 'image', 'image_url',
            'category', 'tags', 'created_at', 'updated_at',
            'average_rating', 'user_rating',
        ]
        read_only_fields = ['created_at', 'updated_at', 'image_url']

        from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'description', 'image', 'category', 'tags']

    def validate_category(self, value):
        allowed_categories = ['Nature', 'Urban', 'Portrait', 'Event', 'Landscape']
        if value and value not in allowed_categories:
            raise serializers.ValidationError("Invalid category")
        return value


    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = PhotoRating.objects.filter(photo=obj, user=request.user).first()
            return rating.rating if rating else None
        return None

    def validate_image(self, value):
        """
        Validate the uploaded image file for Cloudinary compatibility.
        """
        valid_image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        file_extension = value.name.split('.')[-1].lower()

        if file_extension not in valid_image_extensions:
            raise serializers.ValidationError(
                "Invalid file format. Please upload a valid image file (JPEG, PNG, or GIF)."
            )

        max_file_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_file_size:
            raise serializers.ValidationError(
                "The file size exceeds the 10MB limit. Please upload a smaller file."
            )

        return value


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'photo', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    photo = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Photo.objects.all(),
        required=False,  # Make it optional
    )

    class Meta:
        model = Comment
        fields = ['id', 'photo', 'user', 'content', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Ignore 'photo' during updates
        validated_data.pop('photo', None)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
