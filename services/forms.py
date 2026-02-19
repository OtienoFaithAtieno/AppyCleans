
from django import forms
from .models import Booking, DeliveryRequest, LaundryPickup
from .models import Contact
from django.utils import timezone

"""class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name',
            'email',
            'phone',
            'service',
            'date',
            'time',
            'special_requests',
            'status',
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'special_requests': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Any special requests?'
              }),
              'status': forms.Select(attrs={
                  'class': 'form-select'
              }),
        }"""
        
class BookingForm(forms.ModelForm):
    class Meta:
          model = Booking
          fields = ['name', 'email', 'phone', 'service', 'date', 'time', 'special_requests']
          widgets = {
                  'date': forms.DateInput(attrs={'type': 'date'}),
                  'time': forms.TimeInput(attrs={'type': 'time'}),
                  'special_requests': forms.Textarea(attrs={'rows': 3}),
              }

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        today = timezone.now().date()
        return selected_date

        if selected_date < today:
            raise forms.ValidationError("You cannot book a service in the past.")


    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['service'].empty_label = "Select a Service"
         self.fields['date'].widget.attrs['min'] = timezone.now().date()

    def clean(self):
         cleaned_data = super().clean()
         service = cleaned_data.get('service')
         date = cleaned_data.get('date')
         time = cleaned_data.get('time')

         if date == timezone.now().date() and time:
             current_time = timezone.now().time()
             if time < current_time:
                 raise forms.ValidationError("You cannot book a time that has already passed today.")

         if service and date and time:
             exists = Booking.objects.filter(
               service=service,
               date=date,
               time=time
            ).exists()

         if exists:
             raise forms.ValidationError(
                 "This service is already booked at the selected date and time."
             )

         return cleaned_data

class ContactForm(forms.ModelForm):
   class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class LaundryPickupForm(forms.ModelForm):
    class Meta:
        model = LaundryPickup
        fields = ['address', 'pickup_date', 'pickup_time', 'special_instructions']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class DeliveryRequestForm(forms.ModelForm):
    class Meta:
        model = DeliveryRequest
        fields = ['pickup_address', 'delivery_address', 'delivery_date', 'delivery_time', 'notes']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
        }
