from django import forms

from apps.projects.models import Project
from apps.tenants.models import TenantUser
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'due_date', 'estimated_hours', 'actual_hours']

    def __init__(self, *args, tenant=None, **kwargs):
        self.tenant = tenant
        super().__init__(*args, **kwargs)
        if tenant is not None:
            self.fields['project'].queryset = Project.objects.filter(tenant=tenant)
            self.fields['assigned_to'].queryset = TenantUser.objects.filter(tenant=tenant, is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        assigned_to = cleaned_data.get('assigned_to')

        if project and project.tenant != self.tenant:
            raise forms.ValidationError('Invalid project for current tenant.')
        if assigned_to and assigned_to.tenant != self.tenant:
            raise forms.ValidationError('Invalid assignee for current tenant.')
        return cleaned_data
