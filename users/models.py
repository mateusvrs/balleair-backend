from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Personalized General User Model
    """
    is_airline = models.BooleanField(default=False)
    is_traveler = models.BooleanField(default=False)


class Airline(models.Model):
    """
    Airline User Model
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    trade_name = models.CharField(max_length=150, unique=True, blank=False)
    official_name = models.CharField(max_length=150, unique=True, blank=False)
    acronym = models.CharField(max_length=3, unique=True, blank=False)


class Traveler(models.Model):
    """
    Traveler User Model
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
