from django.db import models
from users.models import CustomUser, CarDetails
from posttrip.models import TripDetails
from django.utils import timezone

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
    

class Review(models.Model):
    trip = models.ForeignKey(TripDetails, on_delete=models.CASCADE, related_name='%(class)s_reviews')
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_reviews_given')
    rating = models.IntegerField(default=1)
    review_text = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class CarReview(Review):
    car = models.ForeignKey(CarDetails, on_delete=models.CASCADE, related_name='car_reviews_received')

    def __str__(self):
        return f"Car review by {self.passenger.fullname} for car {self.car.carmodelname}"

class DriverReview(Review):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='driver_reviews_received')

    def __str__(self) -> str:
        return f"Driver review by {self.passenger.fullname} for the trip from {self.trip.startingpoint} to {self.trip.endpoint} by {self.driver.fullname}"

