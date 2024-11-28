from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message objects.
    Includes fields for sender, recipient, subject, body, and timestamps.
    """
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'subject', 'body',
            'is_read', 'created_at', 'updated_at',
        ]
        read_only_fields = ['sender', 'created_at', 'updated_at']
