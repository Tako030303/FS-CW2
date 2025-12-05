from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import Property
from .forms import PropertyForm

def property_listing(request):
    properties = Property.objects.filter(is_active=True)
    
    search_query = request.GET.get('search', '')
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(street__icontains=search_query) |
            Q(about__icontains=search_query)
        )
    listing_type = request.GET.get('listing_type', '')
    if listing_type:
        properties = properties.filter(listing_type=listing_type)
    beds = request.GET.get('beds', '')
    if beds:
        properties = properties.filter(beds__gte=beds)
    
    max_price = request.GET.get('max_price', '')
    if max_price:
        properties = properties.filter(price__lte=max_price)
    sort_by = request.GET.get('sort', '-created_on')
    valid_sorts = ['price', '-price', 'created_on', '-created_on']
    if sort_by in valid_sorts:
        properties = properties.order_by(sort_by)
    else:
        properties = properties.order_by('-created_on')
    context = {
        'properties': properties,
        'search_query': search_query,
        'listing_type': listing_type,
        'beds': beds,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, "properties/listing.html", context)

def property_details(request, pk):
    return render(request, 'properties/details.html', {'property': Property.objects.get(pk=pk)})

@permission_required('properties.view_property', raise_exception=True)
def manage_list(request):
    properties = Property.objects.all()
    return render(request, 'properties/manage_list.html', {'properties': properties})

@permission_required('properties.delete_property', raise_exception=True)
def property_delete(request, pk):
    property_obj = Property.objects.get(pk=pk)
    property_obj.delete()
    messages.success(request, f'Property "{property_obj.title}" deleted.')
    return redirect('properties:manage_list')

@permission_required('properties.add_property', raise_exception=True)
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.created_by = request.user
            property_obj.updated_by = request.user
            property_obj.save()
            messages.success(request, f'Property "{property_obj.title}" created.')
            return redirect('properties:manage_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form})

@permission_required('properties.change_property', raise_exception=True)
def property_edit(request, pk):
    property_obj = Property.objects.get(pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.updated_by = request.user
            property_obj.save()
            messages.success(request, f'Property "{property_obj.title}" updated.')
            return redirect('properties:manage_list')
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'properties/property_form.html', {'form': form})
