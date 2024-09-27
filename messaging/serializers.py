from rest_framework import serializers
from .models import messaging

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = messaging
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'is_read', 'created_at', 'updated_at']
        read_only_fields = ['sender', 'created_at', 'updated_at']