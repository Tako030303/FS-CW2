from django.contrib import admin
from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path('listing/', views.property_listing, name="listing"),
    path('details/<int:pk>/', views.property_details, name="details"),
    path('manage/', views.manage_list, name="manage_list"),
    path('create/', views.property_create, name="create"),
    path('<int:pk>/edit/', views.property_edit, name="edit"),
    path('<int:pk>/delete/', views.property_delete, name="delete"),
]