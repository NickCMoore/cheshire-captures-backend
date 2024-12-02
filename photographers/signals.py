from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Photographer

@receiver(post_save, sender=User)
def create_photographer(sender, instance, created, **kwargs):
    """Create a Photographer for a new User."""
    if created:
        Photographer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_photographer(sender, instance, **kwargs):
    """Save the Photographer when the User is saved."""
    if hasattr(instance, 'photographer'):
        instance.photographer.save()
S