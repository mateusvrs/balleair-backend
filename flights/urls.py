from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_root, name='flights-api-root'),
    
    path('create/', views.CreateFlightView.as_view(), name='create-flight'),
    path('list/', views.ListFlightView.as_view(), name='list-flight'),
    path('detail/<str:pk>/', views.DetailFlightView.as_view(), name='detail-flight'),
    path('retrieve/', views.RetrieveFlightsView.as_view(), name='retrieve-flight'),

    path('book/<str:pk>/', views.BookFlightView.as_view(), name='book-flight'),
    path('cancel/<str:pk>/', views.CancelBookflightView.as_view(), name='cancel-flight'),

    path('airports/', views.AirportsView.as_view(), name='list-airport'),
    path('aircrafts/', views.AircraftsView.as_view(), name='list-aircraft')
]
