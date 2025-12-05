from django.db import models
class Analytics(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ('view_analytics', 'Can view analytics dashboard'),
        ]
