from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.shortcuts import get_object_or_404
from .models import Photographer, Follow
from .serializers import PhotographerSerializer
from rest_framework.permissions import IsAuthenticated

class PhotographerList(generics.ListAPIView):
    queryset = Photographer.objects.annotate(total_followers=Count('followers')).order_by('-total_followers')
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PhotographerDetail(generics.RetrieveUpdateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FollowPhotographerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        photographer = get_object_or_404(Photographer, pk=pk)
        follower = request.user.photographer

        if Follow.objects.filter(follower=follower, following=photographer).exists():
            return Response({'detail': 'You are already following this photographer.'}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=follower, following=photographer)
        return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        photographer = get_object_or_404(Photographer, pk=pk)
        follower = request.user.photographer

        follow_instance = Follow.objects.filter(follower=follower, following=photographer).first()
        if not follow_instance:
            return Response({'detail': 'You are not following this photographer.'}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({'status': 'unfollowed'}, status=status.HTTP_204_NO_CONTENT)

class TopPhotographersView(generics.ListAPIView):
    serializer_class = PhotographerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Photographer.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')
