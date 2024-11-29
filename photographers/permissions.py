from rest_framework import permissions
from messaging.models import Message

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if isinstance(obj, Message):
            return obj.sender.user == request.user

        return obj.user == request.user