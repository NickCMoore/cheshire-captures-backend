from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from photographers.permissions import IsOwnerOrReadOnly

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user.photographer
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.photographer)
