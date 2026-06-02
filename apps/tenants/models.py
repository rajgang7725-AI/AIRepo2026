from django.conf import settings
from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TenantUser(models.Model):
    ROLE_ADMIN = 'ADMIN'
    ROLE_PM = 'PM'
    ROLE_MEMBER = 'MEMBER'
    ROLE_VIEWER = 'VIEWER'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_PM, 'Project Manager'),
        (ROLE_MEMBER, 'Team Member'),
        (ROLE_VIEWER, 'Viewer'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenantuser')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tenant')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
