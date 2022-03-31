from django.db import models

from users.models import Airline, Traveler

from .models_custom import airport_choices, aircraft_choices

class Pax(models.Model):
    """
    Pax Model for Flight Model
    """
    available = models.IntegerField(blank=False)
    booked = models.IntegerField(default=0)


class Flight(models.Model):
    """
    Flight Model
    """
    airline = models.ForeignKey(Airline, related_name='airline_flights', blank=False, on_delete=models.CASCADE)
    travelers = models.ManyToManyField(Traveler, related_name='traveler_flights', blank=True)
    flight_number = models.CharField(max_length=256, blank=False, unique=True, primary_key=True)
    departure_airport = models.CharField(max_length=5, choices=airport_choices(), blank=False)
    arrival_airport = models.CharField(max_length=5, choices=airport_choices(), blank=False)
    flight_date = models.DateTimeField(blank=False)
    aircraft = models.CharField(max_length=6, choices=aircraft_choices(), blank=False)
    pax = models.OneToOneField(Pax, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.pax.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
