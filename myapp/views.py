from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm, BookingForm, VehicleForm, CustomUserChangeForm
from .models import  ParkingSpace, ParkingLot, Vehicle, Booking, User
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import *
from django.contrib.auth import update_session_auth_hash
from django.db.models import F



# Create your views here.

def home(request):
    user = request.user
    vehicles = user.vehicle_set.all()

    vehicle_data = []
    for vehicle in vehicles:
        latest_booking = vehicle.booking_set.order_by('-start_time').first()
        if latest_booking:
            vehicle_data.append({
                'vehicle_number': vehicle.vehicle_number,
                'parking_lot': latest_booking.parking_space.parking_lot.name,
                'parking_space': latest_booking.parking_space.spot_number,
                'latest_booking_id': latest_booking.id  
            })
        else:
            vehicle_data.append({
                'vehicle_number': vehicle.vehicle_number,
                'parking_lot': 'Not Parked',
                'parking_space': 'Not Parked'
            })

    context = {'vehicle_data': vehicle_data}
    return render(request, 'home.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    messages.success(request, 'Successfuly Canceled')

    return redirect('home')

def book_parking(request, parking_lot_id):
    user = request.user
    parking_lot = get_object_or_404(ParkingLot, pk=parking_lot_id)
    available_spaces = ParkingSpace.objects.filter(parking_lot=parking_lot, is_occupied=False)
    available_vehicles = Vehicle.objects.filter(user=user, is_parked=False)

    if request.method == 'POST':
        form = BookingForm(request.POST, user=user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = user
            booking.parking_space = form.cleaned_data['parking_space']
            booking.vehicle = form.cleaned_data['vehicle']

            booking.parking_space.is_occupied = True
            booking.parking_space.save()
            booking.vehicle.is_parked = True
            booking.vehicle.save()

            booking.save()
            
            ParkingLot.objects.filter(pk=parking_lot.id).update(revenue=F('revenue') + booking.cost)

            messages.success(request, 'Your booking for vehicle {} at parking space {} has been confirmed.\n10$ has been deducted from your balance'.format(booking.vehicle.vehicle_number, booking.parking_space.spot_number))
            return redirect('home')
    else:
        form = BookingForm(initial={'parking_lot': parking_lot}, user=user)
        form.fields['parking_space'].queryset = available_spaces
        form.fields['vehicle'].queryset = available_vehicles
    return render(request, 'book_parking.html', {'form': form})

def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)  
            vehicle.user = request.user  
            vehicle.save()
            messages.success(request, 'Successfuly Added')

            return redirect('home')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})


def select_parking_lot(request):
    parking_lots = ParkingLot.objects.all()
    return render(request, 'select_parking_lot.html', {'parking_lots': parking_lots})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash

def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            messages.success(request, 'Successfuly Edited Profile')
            return redirect('home')  
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('login')  
    return render(request, 'delete_profile.html', {'user': request.user})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfuly Changed Password')
            return redirect('home')  
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
def my_parking_lots(request):
    user = request.user  
    parking_lots = ParkingLot.objects.filter(user=user)  

    parking_lots_with_spaces = []
    for lot in parking_lots:
        spaces = lot.parkingspace_set.all()  
        parking_lots_with_spaces.append({
            'lot': lot,
            'spaces': spaces
        })

    bookings = Booking.objects.filter(user=user)

    return render(request, 'my_parking_lots.html', {
        'parking_lots_with_spaces': parking_lots_with_spaces,
        'bookings': bookings
    })