from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(
        upload_to='images/', 
        default='../zjadqskisbjlyfb5jb8i'
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

class Follow(models.Model):
    follower = models.ForeignKey(Photographer, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Photographer, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"