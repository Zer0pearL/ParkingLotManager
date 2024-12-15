from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Vehicle, Booking, ParkingSpace, User

class LoginForm(AuthenticationForm):
    pass

class RegistrationForm(UserCreationForm):
    pass

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle', 'parking_space', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(user=user, is_parked=False)
        self.fields['vehicle'].label_from_instance = lambda obj: obj.vehicle_number
        self.fields['parking_space'].label_from_instance = lambda obj: f"Parking Space: {obj.spot_number}"


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type']
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')