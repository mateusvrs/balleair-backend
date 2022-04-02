from rest_framework import serializers

from .models import Flight, Pax

from datetime import datetime, timedelta
import pytz

class PaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pax
        fields = ['available', 'booked']
        extra_kwargs = {'booked': {'read_only': True}}


class FlightSerializer(serializers.ModelSerializer):
    pax = PaxSerializer(required=True)
    airline = serializers.ReadOnlyField(source='airline.official_name')

    class Meta:
        model = Flight
        fields = '__all__'
        extra_kwargs = {'flight_number': {'read_only': True}, 'travelers': {'read_only': True}}
    
    def create(self, validated_data):
        pax_data = validated_data['pax']
        pax_instance = Pax(available=pax_data['available'])
        pax_instance.save()

        validated_data['pax'] = pax_instance
        return Flight.objects.create(**validated_data)

    def validate(self, data):
        if data.get('departure_airport') == data.get('arrival_airport'):
            raise serializers.ValidationError("Airports need to be different.", code='departure_arrival_airport')

        if data.get('flight_date') <= pytz.utc.localize(datetime.now() + timedelta(hours=12)):
            raise serializers.ValidationError("The flight date must be at least 12h in the future", code='flight_date')

        return data
