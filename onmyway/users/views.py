from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
import re
from .models import CustomUser, UserFiles, CarDetails
from posttrip.models import TripDetails
from findtrip.models import BookingTrip
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from dotenv import load_dotenv
from decouple import config
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


load_dotenv()

client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
verify = client.verify.services(config('TWILIO_VERIFY_SERVICE_SID'))

def send(phone):
    verify.verifications.create(to=phone, channel='sms')

def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
        print("set", result)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'


def homepage(request):
    return render(request, 'users/homepage.html')


def register(request):
    errors = []
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = '+91' + request.POST['phone']
        usertype = request.POST['usertype']
        govtid = request.FILES.get('govt_id', None)
        license = request.FILES.get('license', None)
        vehiclecertificate = request.FILES.get('vehiclecertificate', None)
        password = request.POST['pass']
        confpassword = request.POST['confpass']
        profile_picture = request.FILES.get('profile_picture', None)

        if password != confpassword:
            errors.append('Passwords do not match.')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')

        if not re.match(r'^\+91[6-9][0-9]{9}$', phone):
            errors.append('Please enter a valid phone number.')

        if len(password) < 6:
            errors.append('Password should be at least 6 characters long.')

        if not any(char.isalpha() for char in password):
            errors.append('Password should contain at least one letter.')

        if not any(char.isdigit() for char in password):
            errors.append('Password should contain at least one digit.')

        if CustomUser.objects.filter(email=email).exists():
            errors.append('Email already exists')

        if CustomUser.objects.filter(phone=phone).exists():
            errors.append('Phone already exists')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')
        else:
            hashed_password = make_password(password)
            user = CustomUser.objects.create(
                email = email,
                fullname = fullname,
                phone = phone, 
                password = hashed_password,
                usertype = usertype
            )
            if profile_picture:
                user.profilepicture = profile_picture
            user.save()
            userfiles = UserFiles.objects.create(
                userfile = user,
                govtid = govtid,
                license = license,
                vehiclecertificate = vehiclecertificate
            ) 

            if usertype == 'driver':
                carmodelname = request.POST.get('carmodelname')
                seatingcapacity = request.POST.get('cartype')
                carimages = request.FILES.getlist('carimages', None)
                cardetails = CarDetails.objects.create(usercar=user, carmodelname=carmodelname, seatingcapacity=seatingcapacity)

                for index, image in enumerate(carimages):
                    if index == 0:
                        cardetails.image1 = image
                    elif index == 1:
                        cardetails.image2 = image
                    elif index == 2:
                        cardetails.image3 = image
                    else:
                        break
                cardetails.save()

            return redirect('login')
    return render(request, 'users/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('userprofile')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            next_page = request.POST.get('next', '')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('userprofile')
        else:
            messages.error(request, "Invalid email or password. Please try again")
            return redirect('login')
    return render(request, 'users/login.html')

@login_required
def userprofile(request):
    posted_trips = TripDetails.objects.filter(driver=request.user)
    booked_trips = BookingTrip.objects.filter(passenger=request.user)
    canceled_trips = posted_trips.filter(canceled=True)
    posted_trips = posted_trips.filter(canceled=False)
    car_images = []
    for trip in posted_trips:
        car_image = trip.car.image1.url  
        car_images.append(car_image)
    
    booked_trip_details = []
    for booked_trip in booked_trips:
        booked_trip_details.append({
            'booked_trip': booked_trip,
            'trip_details': booked_trip.trip
        })
    return render(request, 'users/userprofile.html', {
        'posted_trips': posted_trips,
        'car_images': car_images, 
        'booked_trip_details': booked_trip_details,
        'canceled_trips':canceled_trips})

@login_required
def updateprofile(request):
    user = request.user
    errors = []
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = '+91' + request.POST['phone']
        usertype = request.POST['usertype']
        govtid = request.FILES.get('govt_id', None)
        license = request.FILES.get('license', None)
        vehiclecertificate = request.FILES.get('vehiclecertificate', None)
        profile_picture = request.FILES.get('profile_picture', None)
        carmodelname = request.POST['carmodelname']
        seatingcapacity = request.POST['cartype']
        carimages = request.FILES.getlist('carimages', None)

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please enter a valid email address.')

        if not re.match(r'^\+91[6-9][0-9]{9}$', phone):
            errors.append('Please enter a valid phone number.')

        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            errors.append('Email already exists')

        if CustomUser.objects.filter(phone=phone).exclude(pk=user.pk).exists():
            errors.append('Phone already exists')

        if errors:
            for error in errors:
                messages.error(request, error)
                return redirect('updateprofile')
        else:
            user.fullname = fullname
            user.email = email
            user.phone = phone
            user.usertype = usertype
            if profile_picture:
                user.profilepicture = profile_picture
            user.save()

            userfile, created = UserFiles.objects.get_or_create(userfile=user)
            if govtid:
                userfile.govtid = govtid
            if license:
                userfile.license = license
            if vehiclecertificate:
                userfile.vehiclecertificate = vehiclecertificate
            userfile.save()

            usercar, created = CarDetails.objects.get_or_create(usercar=user)
            print(carmodelname, seatingcapacity)
            usercar.carmodelname =  carmodelname
            usercar.seatingcapacity= seatingcapacity
            if carimages:
                for index, image in enumerate(carimages):
                    if index == 0:
                        usercar.image1 = image
                    elif index == 1:
                        usercar.image2 = image
                    elif index == 2:
                        usercar.image3 = image
                    else:
                        break
            usercar.save()
            
            return redirect('userprofile')

    return render(request, 'users/updateprofile.html', {'user': user})


def user_logout(request):
    logout(request)
    return redirect('login')

def forgotpassword(request):
    if request.method == 'POST':
        phone_number = "+91" + request.POST.get('phone')
        print(phone_number)
        try:
            user = CustomUser.objects.get(phone=phone_number)
            if user:
                send(phone_number)
                return render(request, 'users/otpverification.html', {'phone': phone_number})
        except CustomUser.DoesNotExist:
            messages.error(request, "User with the provided phone number doesn't exist.")   
              
    return render(request, 'users/forgotpassword.html')

def otp_verification(request, phone):
    user = CustomUser.objects.get(phone=phone)
    if request.method == 'POST':
        otp_code = request.POST.get('otp')

        if check(phone, otp_code):
            return redirect('resetpassword', phone)
        else:
            messages.error(request, "Please enter the correct otp")
            return render(request, 'users/otpverification.html', {'phone':phone})

    return render(request, 'users/otpverification.html')

def resetpassword(request, phone):
    user = CustomUser.objects.get(phone=phone)
    message = []
    if request.method == 'POST':
        new_password = request.POST['newpassword']
        confnew_password = request.POST['confnewpassword']
        
        if new_password != confnew_password:
            message.append(('Password do not match.', 'error'))
        
        if len(new_password) < 6:
            message.append(('Password should be at least 6 character long.', 'error'))
        
        if not any(char.isalpha() for char in new_password):
            message.append(('Password should contain at least one letter.', 'error'))

        if not any(char.isdigit() for char in new_password):
            message.append(('Password should contain at least one digit.', 'error'))

        if message:
            for msg, tag in message:
                messages.add_message(request, messages.ERROR if tag == 'error' else messages.SUCCESS, msg)
            return redirect('resetpassword', phone)
        else:
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            return redirect('login')
    return render(request,'users/resetpassword.html', {'phone':phone})

@login_required
def changepassword(request):
    message = []
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confnew_password = request.POST['confnewpassword']

        user = request.user
        if not user.check_password(current_password):
            message.append(('Current password is incorrect.', 'error'))
        
        if new_password != confnew_password:
            message.append(('Password do not match.', 'error'))
        
        if len(new_password) < 6:
            message.append(('Password should be at least 6 character long.', 'error'))
        
        if not any(char.isalpha() for char in new_password):
            message.append(('Password should contain at least one letter.', 'error'))

        if not any(char.isdigit() for char in new_password):
            message.append(('Password should contain at least one digit.', 'error'))

        if message:
            for msg, tag in message:
                messages.add_message(request, messages.ERROR if tag == 'error' else messages.SUCCESS, msg)
            return redirect('changepassword')
        else:
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            messages.success(request, 'Password has been successfully changed', 'success')
            update_session_auth_hash(request, user)
            return redirect('userprofile')
            
    return render(request, 'users/changepassword.html')

@login_required
def delete_car_details(request):
    if request.method == 'POST':
        car = CarDetails.objects.filter(usercar=request.user)
        if car.exists():
            car.delete()
            messages.success(request, 'Your car details have been successfully deleted. Please add details for posting trips.')
        else:
            messages.error(request, 'No car details added. Please add details for posting trips. ')
        return redirect('updateprofile')
    return render(request, 'users/updateprofie.html')

def notifications(request):
    return render(request, 'users/notifications.html')