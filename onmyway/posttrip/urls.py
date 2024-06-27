from . import views
from django.urls import path


urlpatterns = [
    path('', views.post, name='post'),
    path('posttrip', views.posttrip, name='posttrip'),
    path('calculate_seat_price', views.calculate_seat_price, name='calculate_seat_price'),
    path('tripdetails/<int:tripid>/', views.tripdetails, name='tripdetails'),
    path('edittrip/<int:tripid>/', views.edittrip, name='edittrip'),
    path('canceltrip/<int:tripid>/', views.canceltrip, name='canceltrip'),
]