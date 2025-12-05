from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from .models import Appointment
from .forms import AppointmentForm
from properties.models import Property

@login_required
def book_appointment(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id, is_active=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property_obj
            appointment.customer = request.user
            appointment.status = 'pending'
            appointment.created_at = timezone.now()
            appointment.save()
            messages.success(request, f'Appointment request sent for {property_obj.title}. A manager will review your request.')
            return redirect('properties:details', pk=property_id)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book.html', {
        'form': form,
        'property': property_obj
    })

@permission_required('appointments.change_appointment', raise_exception=True)
def update_appointment_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    if status not in ['accepted', 'denied', 'completed']:
        messages.error(request, 'Invalid status.')
        return redirect('accounts:profile')
    appointment.status = status
    appointment.updated_at = timezone.now()
    if status == 'accepted':
        appointment.manager = request.user
    appointment.save()
    status_messages = {
        'accepted': f'Appointment for {appointment.property.title} has been accepted.',
        'denied': f'Appointment for {appointment.property.title} has been denied.',
        'completed': f'Appointment for {appointment.property.title} marked as completed.'
    }
    messages.success(request, status_messages.get(status, 'Appointment updated.'))
    return redirect('accounts:profile')

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if appointment.customer != request.user:
        raise PermissionDenied("You can only cancel your own appointments.")
    if appointment.status not in ['pending']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('accounts:profile')
    appointment.status = 'cancelled'
    appointment.updated_at = timezone.now()
    appointment.save()
    messages.success(request, f'Your appointment for {appointment.property.title} has been cancelled.')
    return redirect('accounts:profile')