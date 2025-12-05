from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    is_active = forms.ChoiceField(
        choices=[(True, 'Active'), (False, 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )
    
    class Meta:
        model = Property
        fields = ['title', 'price', 'listing_type', 'district', 'street', 
                  'house_number', 'beds', 'bathrooms', 'area_sqm', 
                  'description', 'provider_name', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Property Image',
            'area_sqm': 'Area (sqm)',
        }
