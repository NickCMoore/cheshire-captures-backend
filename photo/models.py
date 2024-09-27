from django.db import models
from photographers.models import Photographer  # Import Photographer model from photographers app

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Photo(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, related_name='photos', blank=True) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Like(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('photographer', 'photo')

    def __str__(self):
        return f"{self.photographer.user.username} likes {self.photo.title}"

