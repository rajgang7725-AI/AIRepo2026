from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.common.decorators import role_required, tenant_required
from .models import Project


class TenantProjectMixin:
    model = Project

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.tenant is None:
            return queryset.none()
        return queryset.filter(tenant=self.request.tenant)

    def form_valid(self, form):
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)


@method_decorator([login_required, tenant_required], name='dispatch')
class ProjectListView(TenantProjectMixin, ListView):
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'


@method_decorator([login_required, tenant_required], name='dispatch')
class ProjectDetailView(TenantProjectMixin, DetailView):
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class ProjectCreateView(TenantProjectMixin, CreateView):
    template_name = 'projects/project_form.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('project_list')


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class ProjectUpdateView(TenantProjectMixin, UpdateView):
    template_name = 'projects/project_form.html'
    fields = ['name', 'description', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('project_list')


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class ProjectDeleteView(TenantProjectMixin, DeleteView):
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
