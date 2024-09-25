from django.db import models
from photographers.models import Photographer

class Photo(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=100, blank=True) 
    tags = models.ManyToManyField('Tag', blank=True)  

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title


