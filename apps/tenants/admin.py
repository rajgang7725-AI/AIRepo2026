from django.contrib import admin
from .models import Tenant, TenantUser


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tenant', 'role', 'is_active')
    list_filter = ('role', 'tenant', 'is_active')
    search_fields = ('user__username', 'user__email', 'tenant__name')
