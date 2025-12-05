from django.shortcuts import render
from django.db import models
from django.db.models import Avg, Count, Min, Max
from properties.models import Property
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required


def get_average_price_by_district():
    return Property.objects.filter(is_active=True).values('district').annotate(
        avg_price=Avg('price'),
        property_count=Count('id'),
        min_price=Min('price'),
        max_price=Max('price')
    ).order_by('-avg_price')



def get_general_statistics():
    total_properties = Property.objects.filter(is_active=True).count()
    total_districts = Property.objects.filter(is_active=True).values('district').distinct().count()
    avg_price = Property.objects.filter(is_active=True).aggregate(avg=Avg('price'))['avg']
    
    return {
        'total_properties': total_properties,
        'total_districts': total_districts,
        'average_price': avg_price,
    }


def get_manager_appointment_stats():
    managers = User.objects.filter(
        models.Q(appointments_manager__isnull=False) |
        models.Q(groups__name__in=['Manager', 'Staff'])
    ).distinct().annotate(
        total_appointments=Count('appointments_manager'),
        accepted_count=Count('appointments_manager', filter=models.Q(appointments_manager__status='accepted')),
        denied_count=Count('appointments_manager', filter=models.Q(appointments_manager__status='denied')),
        completed_count=Count('appointments_manager', filter=models.Q(appointments_manager__status='completed'))
    ).filter(total_appointments__gt=0).order_by('-total_appointments')
    
    return managers


@permission_required('analytics.view_analytics', raise_exception=True)
def analytics_dashboard(request):
    context = {
        'general_stats': get_general_statistics(),
        'district_stats': get_average_price_by_district(),
        'manager_stats': get_manager_appointment_stats(),
    }
    return render(request, 'analytics/dashboard.html', context)