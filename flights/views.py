from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from .serializers import FlightSerializer
from .models import Flight
from .permissions import IsAuthenticatedWithAirline, IsAuthenticatedWithTraveler, IsFlightOwner
from .views_functions import create_new_flight_number

from users.models import Airline, Traveler

from datetime import datetime, timedelta
import pytz


## APi root ##

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'create': reverse('create-flight', request=request, format=format),
        'list': reverse('list-flight', request=request, format=format),
        'airports': reverse('list-airport', request=request, format=format),
        'aircrafts': reverse('list-aircraft', request=request, format=format),
    })


## Handle Flight ##

class CreateFlightView(generics.CreateAPIView):
    """
    Create flight with an airline token authentication
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedWithAirline]

    def perform_create(self, serializer):
        airline = Airline.objects.get(pk=self.request.user)
        new_flight_number = create_new_flight_number(airline)
        serializer.save(airline=airline, flight_number=new_flight_number)


class ListFlightView(generics.ListAPIView):
    """
    List all flights with any user type token authentication
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetailFlightView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handle specific flight with an airline token authentication and being flight owner
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedWithAirline, IsFlightOwner]


class BookFlightView(generics.GenericAPIView):
    """
    Book flight with a traveler token authentication
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedWithTraveler]
    
    def get(self, request, *args, **kwargs):
        flight_number = self.kwargs.get('pk')
        current_user = Traveler.objects.get(pk=request.user)
        
        try:
            flight = self.get_queryset().get(pk=flight_number)
        except:
            return Response({'response': 'This flight does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        if flight.flight_date < pytz.utc.localize(datetime.now() + timedelta(hours=1)):
            return Response({'response': "Sorry, you can only book a flight 1h before"}, status=status.HTTP_400_BAD_REQUEST)

        if current_user in flight.travelers.all():
            return Response({'response': "You have already booked this flight"}, status=status.HTTP_400_BAD_REQUEST)

        if flight.pax.booked == flight.pax.available:
            return Response({'response': 'The flight is already full'}, status=status.HTTP_400_BAD_REQUEST)

        flight.travelers.add(current_user)
        flight.pax.booked += 1
        flight.pax.save()
        flight.save()
        return Response({'response': 'The flight has been booked'}, status=status.HTTP_200_OK)


class CancelBookflightView(generics.GenericAPIView):
    """
    Cancel flight with traveler token authentication
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticatedWithTraveler]
    
    def get(self, request, *args, **kwargs):
        flight_number = self.kwargs.get('pk')
        current_user = Traveler.objects.get(pk=request.user)
        
        try:
            flight = self.get_queryset().get(pk=flight_number)
        except:
            return Response({'response': 'This flight does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        if current_user not in flight.travelers.all():
            return Response({'response': "You don't have booked yet"}, status=status.HTTP_400_BAD_REQUEST)
        
        flight.travelers.remove(current_user)
        flight.pax.booked -= 1
        flight.pax.save()
        flight.save()
        return Response({'response': 'Flight booking has been canceled'}, status=status.HTTP_200_OK)


class RetrieveFlightsView(generics.ListAPIView):
    """
    Retrieve a list of specific flights based on some query parameters
    """
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        filter_options = {}

        departure_airport = self.request.query_params['departure_airport']
        if departure_airport:
            filter_options['departure_airport'] = departure_airport

        arrival_airport = self.request.query_params['arrival_airport']
        if arrival_airport:
            filter_options['arrival_airport'] = arrival_airport
        
        airline = self.request.query_params['airline']
        if airline:
            filter_options['airline'] = airline

        flight_date = self.request.query_params['flight_date']
        if flight_date:
            flight_date_array = list(map(int, flight_date.split('-')))
            start_flight_date = datetime(year=flight_date_array[0], month=flight_date_array[1], day=flight_date_array[2])
            end_flight_date = start_flight_date + timedelta(hours=23, minutes=59, seconds=59)
            flight_date_range = [pytz.utc.localize(start_flight_date), pytz.utc.localize(end_flight_date)]
            filter_options['flight_date__range'] = flight_date_range

        try:
            return Flight.objects.filter(**filter_options)
        except BaseException as error:
            raise exceptions.ParseError(detail=error)


## List Airports and aircrafts ##

class AirportsView(generics.ListAPIView):
    """
    List all airports available
    """
    queryset = Flight.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            airports = Flight.departure_airport.field.choices
        except:
            return Response({'response': 'Unable to return airport options'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(airports, status=status.HTTP_200_OK)


class AircraftsView(generics.ListAPIView):
    """
    List all aircrafts available
    """
    queryset = Flight.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            aircrafts = Flight.aircraft.field.choices
        except:
            return Response({'response': 'Unable to return aircraft options'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(aircrafts, status=status.HTTP_200_OK)
