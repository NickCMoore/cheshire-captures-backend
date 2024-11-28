from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from photographers.permissions import IsOwnerOrReadOnly


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Message objects.
    Provides list, create, retrieve, update, and delete functionality.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Return messages where the current user is the sender or recipient.
        """
        if not self.request.user.is_authenticated:
            return Message.objects.none()

        user = self.request.user.photographer
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        """
        Automatically set the sender to the current user when creating a message.
        """
        serializer.save(sender=self.request.user.photographer)
