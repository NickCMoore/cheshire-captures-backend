from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    follower_count = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    profile_image = models.ImageField(
        upload_to='images/',
        default='https://res.cloudinary.com/dwgtce0rh/image/upload/v1727862662/vestrahorn-mountains-stokksnes-iceland_aoqbtp.jpg'
    )
    cover_image = models.ImageField(
        upload_to='cover_images/',
        default='https://res.cloudinary.com/dwgtce0rh/image/upload/v1727862662/vestrahorn-mountains-stokksnes-iceland_aoqbtp.jpg'
    )

    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    twitter = models.URLField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Save the Photographer, generating a slug if not present."""
        if not self.slug:
            self.slug = slugify(self.display_name)[:50] + '-' + get_random_string(6)
        super(Photographer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} ({self.user.username})"

class Follow(models.Model):
    follower = models.ForeignKey(Photographer, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(Photographer, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.following.user.username}"
