from django.shortcuts import render, redirect
from posttrip.models import TripDetails
from .models import BookingTrip
from otherpages.models import Notifications
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from datetime import datetime

def find(request):
    trip_details = None
    if request.method == 'POST':
        starting_point = request.POST.get('from')
        ending_point = request.POST.get('to')
        departure_date = request.POST.get('leaving')  

        trip_query = TripDetails.objects.filter(
            startingpoint__icontains=starting_point,
            endpoint__icontains=ending_point,
            canceled=False
        ).select_related('driver', 'car')
        
 
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
                print(departure_date)
                trip_query = trip_query.filter(departuredate=departure_date)
            except ValueError:
                pass
        
        trip_details = trip_query
        
    return render(request, 'findtrip/findtrip.html', {'trip_details': trip_details})

def book(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        try:
            selected_trip = TripDetails.objects.get(pk=trip_id)
        except TripDetails.DoesNotExist:
            messages.error(request, 'Selected trip does not exist.')
            return redirect(reverse('users:userprofile'))

        # Get form data
        no_seats = int(request.POST.get('no_seats'))
        total_price = selected_trip.seatprice * no_seats
        car = selected_trip.car

        # Create BookingTrip object
        booking = BookingTrip.objects.create(
            booking_date=timezone.now().date(),
            booking_time=timezone.now().time(),
            no_seats=no_seats,
            total_price=total_price,
            passenger = request.user,
            car=car,
            trip=selected_trip
        )

        # Update available seats in selected trip
        selected_trip.emptyseats -= no_seats
        selected_trip.save()

        Notifications.passenger_booktrip_notification(request.user, selected_trip)
        Notifications.driver_booktrip_notification(selected_trip.driver, booking)
        return redirect(reverse('userprofile'))  

    else:
        trip_id = request.GET.get('trip_id')
        try:
            selected_trip = TripDetails.objects.get(pk=trip_id)
        except TripDetails.DoesNotExist:
            messages.error(request, 'Selected trip does not exist.')
            return redirect('find')
        available_seats = selected_trip.emptyseats

    return render(request, 'findtrip/booktrip.html', {'selected_trip': selected_trip, 'available_seats': available_seats})