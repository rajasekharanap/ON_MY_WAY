from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BookingTrip
from otherpages.models import Notifications


@shared_task
def send_review_notifications():
    two_days_ago = timezone.now().date() - timedelta(days=2)
    print(two_days_ago)

    booking_to_notify = BookingTrip.objects.filter(trip__departuredate=two_days_ago)
    print('hi')
    for booking in booking_to_notify:
        print(f"Notification for booking ID: {booking.id}")
        Notifications.passenger_review_notifications(booking.passenger, booking.trip)