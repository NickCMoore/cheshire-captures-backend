from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)

    profile_image = models.ImageField(
        upload_to='images/',
        default=settings.DEFAULT_PROFILE_IMAGE_URL
    )
    cover_image = models.ImageField(
        upload_to='cover_images/',
        default=settings.DEFAULT_PROFILE_IMAGE_URL
    )

    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name or self.user.username} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_photographer(sender, instance, created, **kwargs):
    """
    Automatically create a Photographer profile for a new User.
    """
    if created:
        Photographer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_photographer(sender, instance, **kwargs):
    """
    Save the Photographer profile when the User is updated.
    """
    if hasattr(instance, 'photographer'):
        instance.photographer.save()


class Follow(models.Model):
    follower = models.ForeignKey(
        Photographer, related_name='following', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Photographer, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"


@receiver(post_save, sender=Follow)
def update_follower_count_on_create(sender, instance, created, **kwargs):
    """
    Update the follower count of a Photographer when a Follow is created.
    """
    if created:
        instance.following.follower_count += 1
        instance.following.save()


@receiver(post_delete, sender=Follow)
def update_follower_count_on_delete(sender, instance, **kwargs):
    """
    Update the follower count of a Photographer when a Follow is deleted.
    """
    instance.following.follower_count -= 1
    if instance.following.follower_count < 0:
        instance.following.follower_count = 0  # Ensure count doesn't go negative
    instance.following.save()
