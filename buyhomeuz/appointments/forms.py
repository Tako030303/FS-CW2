from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['start_time', 'details']
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'required': True
                }
            ),
            'details': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Any specific requirements or questions? (Optional)'
                }
            ),
        }
        labels = {
            'start_time': 'Preferred Date & Time',
            'details': 'Additional Notes',
        }
