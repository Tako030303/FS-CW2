from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:property_id>/', views.book_appointment, name='book'),
    path('update/<int:pk>/<str:status>/', views.update_appointment_status, name='update_status'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel'),
]