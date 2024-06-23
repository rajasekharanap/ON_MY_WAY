from . import views
from django.urls import path


urlpatterns = [
    path('', views.post, name='post'),
    # path('validate_user/', views.validate_user, name='validate_user'),
    path('tripdetails', views.tripdetails, name='tripdetails'),
    path('calculate_seat_price', views.calculate_seat_price, name='calculate_seat_price')
]