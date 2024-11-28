from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Photo(models.Model):
    photographer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/dwgtce0rh/image/upload/v1727862662/vestrahorn-mountains-stokksnes-iceland_aoqbtp.jpg',
    )
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, related_name='photos', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.photo.title}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.photo.title}"

class PhotoRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rated {self.photo.title} with {self.rating} stars"
