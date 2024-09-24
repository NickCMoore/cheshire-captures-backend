from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='photographer_images/', 
        default='default_images/placeholder.jpg'
    )
    location = models.CharField(max_length=255, blank=True)
    cover_image = models.ImageField(
        upload_to='cover_images/', 
        default='default_images/cover_placeholder.jpg'
    )
    website = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name} ({self.user.username})"

def create_photographer(sender, instance, created, **kwargs):
    if created:
        Photographer.objects.create(user=instance)

post_save.connect(create_photographer, sender=User)
