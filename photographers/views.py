from rest_framework import generics
from .models import Photographer
from .serializers import PhotographerSerializer

class PhotographerList(generics.ListCreateAPIView):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer
