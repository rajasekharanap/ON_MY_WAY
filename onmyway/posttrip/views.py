from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import TripDetails
from users.models import CarDetails
from django.http import JsonResponse


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
def tripdetails(request):
    errors = []
    if request.method == 'POST':
        cardetails = CarDetails.objects.get(usercar=request.user)

        startingpoint = request.POST['startingpoint']
        endpoint = request.POST['ending-point']
        departuredate = request.POST['departure-date']
        departuretime = request.POST['departure-time']
        luggagesize = request.POST['luggage-size']
        pets = request.POST['pets-allowed']
        emptyseats = request.POST['empty-seats']
        kilometers=100
        seatprice = request.POST['seat-price']
        description = request.POST.get('description')

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
    return render(request, 'posttrip/posttrip.html')
