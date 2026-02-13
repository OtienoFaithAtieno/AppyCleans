# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Service, Booking
from .forms import BookingForm
from .forms import ContactForm

def landing(request):
    services = Service.objects.all()
    return render(request, "services/landing.html", {"services": services})

def services_page(request):
    services = Service.objects.all()
    return render(request, "services/services.html", {"services": services})


@login_required
def booking_page(request):
    service_id = request.GET.get('service')

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return render(request, 'services/booking_success.html')
    else:
        initial_data = {}
        if service_id:
            try:
                initial_data['service'] = Service.objects.get(id=service_id)
            except Service.DoesNotExist:
                pass

        form = BookingForm(initial=initial_data)

    return render(request, 'services/booking.html', {'form': form})


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'services/bookingHistory.html', {'bookings': bookings})



def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'services/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'services/contact.html', {'form': form})
