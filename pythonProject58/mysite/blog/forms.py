from django import forms
from .models import Booking, Client, Room, Pet
from django.core.exceptions import ValidationError
from django.utils import timezone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client', 'room', 'arrival_date', 'departure_date', 'human_count', 'pet']
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        arrival_date = cleaned_data.get('arrival_date')
        departure_date = cleaned_data.get('departure_date')
        room = cleaned_data.get('room')

        if arrival_date and departure_date:
            if arrival_date >= departure_date:
                raise ValidationError("Дата выезда должна быть позже даты заезда")

            if arrival_date < timezone.now().date():
                raise ValidationError("Нельзя бронировать номер на прошедшую дату")

            if room and Booking.objects.filter(
                    room=room,
                    arrival_date__lt=departure_date,
                    departure_date__gt=arrival_date,
                    status='действительно'
            ).exists():
                raise ValidationError("Этот номер уже забронирован на выбранные даты")

        return cleaned_data