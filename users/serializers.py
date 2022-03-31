from rest_framework import serializers

from .models import User, Airline, Traveler


class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}


class TravelerSerializer(serializers.ModelSerializer):
    owner = UserSerializer(required=True)
    traveler_flights = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
    airline_flights = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
