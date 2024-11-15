from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Photographer, Follow
from .serializers import PhotographerSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

# List all photographers, ordered by the number of followers
class PhotographerList(generics.ListAPIView):
    queryset = Photographer.objects.filter(user__isnull=False) \
                                   .annotate(total_followers=Count('followers')) \
                                   .order_by('-total_followers')
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PhotographerDetail(generics.RetrieveUpdateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]  # Apply permissions

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Support partial updates
        instance = self.get_object()

        # Permission check is now handled by IsOwnerOrReadOnly
        self.check_object_permissions(request, instance)

        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# API to follow or unfollow a photographer
class FollowPhotographerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        photographer = get_object_or_404(Photographer, pk=pk)
        
        # Check if user has a photographer profile
        try:
            follower = request.user.photographer  
        except Photographer.DoesNotExist:
            return Response({'detail': 'You do not have a photographer profile.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already following
        if Follow.objects.filter(follower=follower, following=photographer).exists():
            return Response({'detail': 'You are already following this photographer.'}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=follower, following=photographer)
        photographer.follower_count += 1  # Update follower count on follow
        photographer.save()
        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        photographer = get_object_or_404(Photographer, pk=pk)

        # Check if user has a photographer profile
        try:
            follower = request.user.photographer  
        except Photographer.DoesNotExist:
            return Response({'detail': 'You do not have a photographer profile.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if not following
        follow_instance = Follow.objects.filter(follower=follower, following=photographer).first()
        if not follow_instance:
            return Response({'detail': 'You are not following this photographer.'}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        photographer.follower_count -= 1  # Update follower count on unfollow
        photographer.save()
        return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)

# List top photographers by the number of followers, excluding deleted users
class TopPhotographersView(generics.ListAPIView):
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Exclude photographers whose user is deleted
        return Photographer.objects.filter(user__isnull=False) \
                                   .annotate(total_followers=Count('followers')) \
                                   .order_by('-total_followers')

# API endpoint to list all followers of a specific photographer
class PhotographerFollowersAPIView(APIView):
    def get(self, request, pk):
        photographer = get_object_or_404(Photographer, pk=pk)
        followers = photographer.followers.all()  # Using the reverse relationship

        followers_list = [{'id': follower.user.id, 'username': follower.user.username} for follower in followers]
        return Response({'followers': followers_list})
