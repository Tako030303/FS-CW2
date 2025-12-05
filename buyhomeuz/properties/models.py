from django.db import models
from django.utils import timezone
from django.conf import settings

class Property(models.Model):
    LISTING_TYPE_CHOICES = (
        ('sale','Sale'),
        ('rent','Rent')
    )
    
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)
    beds = models.IntegerField()
    bathrooms = models.IntegerField()
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    provider_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties_createdby'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties_updatedby'
    )
    image = models.ImageField(upload_to='property_images', blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Properties"
    
    def __str__(self):
        return self.title
