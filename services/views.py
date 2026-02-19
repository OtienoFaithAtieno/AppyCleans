
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Booking
from .forms import BookingForm, LaundryPickupForm, DeliveryRequestForm
from .forms import ContactForm
from django.contrib import messages

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


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status in ['completed', 'cancelled']:
        messages.error(request, "This booking cannot be cancelled.")
    else:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")

    return redirect('booking_history')


@login_required
def reschedule_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.status in ['completed', 'cancelled']:
        messages.error(request, "This booking cannot be modified.")
        return redirect('booking_history')

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking rescheduled successfully.")
            return redirect('booking_history')
    else:
        form = BookingForm(instance=booking)

    return render(request, 'services/reschedule.html', {'form': form})



def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'services/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'services/contact.html', {'form': form})


@login_required
def schedule_pickup(request):
    if request.method == "POST":
        form = LaundryPickupForm(request.POST)
        if form.is_valid():
            pickup = form.save(commit=False)
            pickup.user = request.user
            pickup.save()
            return redirect("booking_history")
    else:
        form = LaundryPickupForm()

    return render(request, "services/schedule_pickup.html", {"form": form})


@login_required
def request_delivery(request):
    if request.method == "POST":
        form = DeliveryRequestForm(request.POST)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.user = request.user
            delivery.save()
            return redirect("booking_history")
    else:
        form = DeliveryRequestForm()

    return render(request, "services/request_delivery.html", {"form": form})
