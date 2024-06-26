from django.db import models
from users.models import CustomUser, CarDetails
from posttrip.models import TripDetails

class BookingTrip(models.Model):
    booking_date = models.DateField()
    booking_time = models.TimeField()
    no_seats = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='booked_trips_as_passenger')
    car = models.ForeignKey(CarDetails, on_delete=models.CASCADE, related_name='booked_trip_car')
    trip = models.ForeignKey(TripDetails, on_delete=models.CASCADE, related_name='bookings')    

    def __str__(self):
        return f"Booking by {self.passenger.email} for trip from {self.trip.startingpoint} to {self.trip.endpoint}"