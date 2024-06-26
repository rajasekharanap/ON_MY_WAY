from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import TripDetails
from users.models import CarDetails
from django.http import JsonResponse
from django.contrib import messages
from findtrip.models import BookingTrip


def post(request):
    return render(request, 'posttrip/posttrip.html')

def calculate_total_kilometers(seating_capacity, total_kms):
    if seating_capacity == 5:
        average_mileage = 15
    else:
        average_mileage = 13

    total_fuel = total_kms / average_mileage
    fuel_cost = 100
    total_cost = total_fuel * fuel_cost
    total_cost = int(total_cost)
    return total_cost

def calculate_seat_price(request):
    try:
        car_details = CarDetails.objects.get(usercar=request.user)
        print(car_details)
    except CarDetails.DoesNotExist:
        return JsonResponse({'error': 'Car details not found'})

    total_kms = request.GET.get('total_kms')
    if not total_kms:
        return JsonResponse({'error': 'Total kilometers not provided'})
    print(total_kms)

    total_kms = float(total_kms)

    seating_capacity = car_details.seatingcapacity
    print(seating_capacity)
    total_cost = calculate_total_kilometers(seating_capacity, total_kms)
    print(total_cost)
    seat_price = int(total_cost / (seating_capacity - 1))
    print(seat_price)
    return JsonResponse({'seat_price': seat_price})



@login_required
def posttrip(request):
    errors = [] 
    max_empty_seats = 6
    cardetails = None
    if request.method == 'POST':
        if request.user.usertype != 'driver':
            errors.append('Please update your usertype to driver for posting trip.')

        try:
            cardetails = CarDetails.objects.get(usercar=request.user)
        except CarDetails.DoesNotExist:
            errors.append('Please add your car details for posting trip.')
        
        if cardetails is not None:
            max_empty_seats = cardetails.seatingcapacity - 1

        startingpoint = request.POST['startingpoint']
        endpoint = request.POST['ending-point']
        departuredate = request.POST['departure-date']
        departuretime = request.POST['departure-time']
        luggagesize = request.POST['luggage-size']
        pets = request.POST['pets-allowed']
        emptyseats = request.POST['empty-seats']
        kilometers= request.POST['kilometers']
        print(kilometers)
        seatprice = request.POST['seat-price']
        description = request.POST.get('description')

        carcapacity = cardetails.seatingcapacity
        if int(emptyseats) > max_empty_seats:
            errors.append(f'Your car seating capacity is {cardetails.seatingcapacity}')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'posttrip/posttrip.html', {'max_empty_seats':max_empty_seats, 'updateprofile_url':reverse('updateprofile'), 'errors':errors})

        else:
            trip_details = TripDetails.objects.create(
                driver = request.user,
                car = cardetails,
                startingpoint = startingpoint,
                endpoint = endpoint,
                departuredate = departuredate,
                departuretime = departuretime,
                luggagesize = luggagesize,
                pets = pets,
                emptyseats = emptyseats,
                kilometers = kilometers,
                seatprice = seatprice,
                description = description
            )
            return redirect(reverse('userprofile'))
    return render(request, 'posttrip/posttrip.html',{'max_empty_seats':max_empty_seats})


def tripdetails(request, tripid):
    tripdetails = get_object_or_404(TripDetails, id=tripid)
    print(tripdetails.id, tripid)
    bookings = BookingTrip.objects.filter(trip=tripdetails)
    passengers_info = [{'passenger':booking.passenger, 'seats_booked':booking.no_seats} for booking in bookings]
    total_seats_booked = sum(booking.no_seats for booking in bookings)
    total_seats_posted = total_seats_booked + tripdetails.emptyseats
    context = {
        'tripdetails':tripdetails,
        'passengers_info':passengers_info,
        'total_seats_booked':total_seats_booked,
        'total_seats_posted':total_seats_posted
    }
    return render(request, 'posttrip/tripdetails.html', context)

def edittrip(request):
    return render(request, 'posttrip/edittrip.html')

@login_required
def canceltrip(request, tripid):
    trip = get_object_or_404(TripDetails, id=tripid)
    trip.delete()
    return redirect(reverse('userprofile'))



