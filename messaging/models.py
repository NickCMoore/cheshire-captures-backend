from django.db import models
from photographers.models import Photographer


class Message(models.Model):
    """
    Model representing a message sent between photographers.
    """
    sender = models.ForeignKey(
        Photographer,
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        Photographer,
        related_name='received_messages',
        on_delete=models.CASCADE,
    )
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the Message object.
        """
        return f"Message from {self.sender.display_name} to {self.recipient.display_name}"
