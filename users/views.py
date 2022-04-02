from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from .models import Traveler, Airline, User
from .serializers import TravelerSerializer, AirlineSerializer, UserSerializer

## APi root ##

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'info': reverse('info-user', request=request, format=format),
        'register-traveler': reverse('register-traveler', request=request, format=format),
        'register-airline': reverse('register-airline', request=request, format=format),
        'obtain-token': reverse('obtain-token', request=request, format=format),
    })


## Register Traveler ##

class RegisterTravelerView(generics.CreateAPIView):
    """
    Register traveler user
    """
    queryset = User.objects.all()
    serializer_class = TravelerSerializer


## Register Airline ##

class RegisterAirlineView(generics.CreateAPIView):
    """
    Register airline user with super user token authentication
    """
    queryset = User.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


## User Handle ##

class ObtainUserInformation(generics.GenericAPIView):
    """
    Obtain user informations with token authentication header
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_traveler:
            return TravelerSerializer
        elif self.request.user.is_airline:
            return AirlineSerializer
        else:
            return UserSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_traveler:
            user = Traveler.objects.get(pk=request.user)
        elif request.user.is_airline:
            user = Airline.objects.get(pk=request.user)
        else:
            user = request.user

        user_serializer = self.get_serializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
