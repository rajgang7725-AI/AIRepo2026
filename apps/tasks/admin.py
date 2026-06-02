from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'tenant', 'assigned_to', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'tenant', 'project')
    search_fields = ('title', 'description', 'project__name', 'assigned_to__user__username')
