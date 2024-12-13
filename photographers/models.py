from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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
        default='../coast'
    )

    cover_image = models.ImageField(
        upload_to='images/', 
        default='../cs99p88tqdy3vf87cikh'
    )

    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name} ({self.user.username})"

@receiver(post_save, sender=User)
def create_photographer(sender, instance, created, **kwargs):
    if created:
        Photographer.objects.create(user=instance)

class Follow(models.Model):
    follower = models.ForeignKey(Photographer, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Photographer, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"

@receiver(post_save, sender=Follow)
def update_follower_count_on_create(sender, instance, created, **kwargs):
    if created:
        instance.following.follower_count += 1
        instance.following.save()

@receiver(post_delete, sender=Follow)
def update_follower_count_on_delete(sender, instance, **kwargs):
    instance.following.follower_count -= 1
    instance.following.save()