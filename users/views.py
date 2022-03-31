from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from .models import User
from .serializers import TravelerSerializer, AirlineSerializer

## APi root ##

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register-traveler': reverse('register-traveler', request=request, format=format),
        'register-airline': reverse('register-airline', request=request, format=format),
        'obtain-token': reverse('obtain-token', request=request, format=format),
        'refresh-token': reverse('refresh-token', request=request, format=format),
    })


## Register Traveler ##

class RegisterTravelerView(generics.CreateAPIView):
    """
    Register Traveler view  - CreateAPIView
    """
    queryset = User.objects.all()
    serializer_class = TravelerSerializer


## Register Airline ##

class RegisterAirlineView(generics.CreateAPIView):
    """
    Register Airline view  - CreateAPIView
    """
    queryset = User.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
