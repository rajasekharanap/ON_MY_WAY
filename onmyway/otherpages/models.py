from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Notification for {self.user.email} created at {self.created_at}"
    
    @classmethod
    def registration_notification(cls, user):
         message = "Welcome to ON MY WAY. Find or Share safe rides with us."
         cls.objects.create(user=user, message=message)

    @classmethod
    def posttrip_notification(cls, driver, trip):
        message = f"You have successfully posted your trip from {trip.startingpoint} to {trip.endpoint}"
        cls.objects.create(user=driver, message=message)

    @classmethod
    def passenger_booktrip_notification(cls, passenger, trip):
        message = f"You have successfully booked a trip from {trip.startingpoint} to {trip.endpoint} on {trip.departuredate}. Contact your driver {trip.driver.name} through {trip.driver.email} or {trip.driver.phone}."
        cls.objects.create(user=passenger, message=message)

    @classmethod
    def driver_booktrip_notification(cls, driver, booking):
        message = f"You trip from {booking.trip.startingpoint} to {booking.trip.endpoint} on {booking.trip.departuredate} has been booked by {booking.passenger.name}. Contact your passenger through {booking.passenger.email} or {booking.passenger.phone}."
        cls.objects.create(user=driver, message=message)

    

