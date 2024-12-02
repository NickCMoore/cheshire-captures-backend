from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Photographer
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_photographer(sender, instance, created, **kwargs):
    """Create a photographer for a new user."""
    if created:
        Photographer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_photographer(sender, instance, **kwargs):
    """Save the photographer for an existing user."""
    instance.photographer.save()
