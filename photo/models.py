from django.db import models
from photographers.models import Photographer

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

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


