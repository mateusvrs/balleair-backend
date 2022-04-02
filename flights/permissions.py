from rest_framework import permissions

from users.models import Airline

class IsAuthenticatedWithAirline(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_airline)


class IsAuthenticatedWithTraveler(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_traveler)


class IsFlightOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        request_airline = Airline.objects.get(pk=request.user)
        return obj.airline == request_airline
