from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    path('', views.api_root, name='users-api-root'),
    
    path('info/', views.ObtainUserInformation.as_view(), name='info-user'),
    path('register/traveler/', views.RegisterTravelerView.as_view(), name='register-traveler'),
    path('register/airline/', views.RegisterAirlineView.as_view(), name='register-airline'),

    path('token/', TokenObtainPairView.as_view(), name='obtain-token'),
]
