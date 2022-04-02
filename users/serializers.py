from rest_framework import serializers

from flights.models import Flight

from .models import User, Airline, Traveler


class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_traveler', 'is_airline']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}, 'is_traveler': {'read_only': True}, 'is_airline': {'read_only': True}}


class UserFlightSerializer(serializers.ModelSerializer):
    airline = serializers.ReadOnlyField(source='airline.official_name')

    class Meta:
        model = Flight
        fields = ['flight_number', 'airline', 'departure_airport', 'arrival_airport', 'flight_date']
        

class TravelerSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=True)
    traveler_flights = UserFlightSerializer(many=True, read_only=True)

    class Meta:
        model = Traveler
        fields = ['owner', 'traveler_flights']
        
    def create(self, validated_data):
        owner = validated_data['owner']
        account = User(
            username=owner['username'],
            email=owner['email']
        )
        account.set_password(owner['password'])
        account.is_traveler = True

        traveler = Traveler(
            owner=account
        )
        
        account.save()
        traveler.save()

        return traveler


class AirlineSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=True)
    airline_flights = UserFlightSerializer(many=True, read_only=True)

    class Meta:
        model = Airline
        fields = ['owner', 'trade_name', 'official_name', 'acronym', 'airline_flights']
        
    def create(self, validated_data):
        owner = validated_data['owner']
        account = User(
            username=owner['username'],
            email=owner['email']
        )
        account.set_password(owner['password'])
        account.is_airline = True
        
        airline = Airline(
            owner=account,
            trade_name=validated_data['trade_name'],
            official_name=validated_data['official_name'],
            acronym=validated_data['acronym']
        )

        account.save()
        airline.save()

        return airline
