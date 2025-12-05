from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from properties.models import Property
from appointments.models import Appointment
from .serializers import UserSerializer, GroupSerializer, PropertySerializer, AppointmentSerializer
from rest_framework.permissions import DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email','first_name','last_name', 'groups']
    search_fields = ['username', 'email','first_name','last_name']
    ordering_fields = ['username', 'email','first_name','last_name']
    permission_classes = [DjangoModelPermissions]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [DjangoModelPermissions]

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'district', 'listing_type', 'is_active']
    search_fields = ['title', 'district']
    ordering_fields = ['title', 'price', 'created_on']
    permission_classes = [DjangoModelPermissions]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'property', 'manager', 'status']
    search_fields = ['details']
    ordering_fields = ['start_time', 'status']
    permission_classes = [DjangoModelPermissions]
