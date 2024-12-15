from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ParkingLot(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


    

class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    spot_number = models.IntegerField()
    is_occupied = models.BooleanField(default=False)


class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)  
    is_parked = models.BooleanField(default=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    def delete(self, *args, **kwargs):
        self.parking_space.is_occupied = False
        self.parking_space.save()
        self.vehicle.is_parked = False
        self.vehicle.save()
        super().delete(*args, **kwargs)