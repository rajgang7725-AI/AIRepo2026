from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.common.decorators import role_required, tenant_required
from .forms import TaskForm
from .models import Task


class TenantTaskMixin:
    model = Task

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.tenant is None:
            return queryset.none()
        return queryset.filter(tenant=self.request.tenant)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tenant'] = self.request.tenant
        return kwargs

    def form_valid(self, form):
        form.instance.tenant = self.request.tenant
        return super().form_valid(form)


@method_decorator([login_required, tenant_required], name='dispatch')
class TaskListView(TenantTaskMixin, ListView):
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


@method_decorator([login_required, tenant_required], name='dispatch')
class TaskDetailView(TenantTaskMixin, DetailView):
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class TaskCreateView(TenantTaskMixin, CreateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class TaskUpdateView(TenantTaskMixin, UpdateView):
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')


@method_decorator([login_required, tenant_required, role_required('ADMIN', 'PM')], name='dispatch')
class TaskDeleteView(TenantTaskMixin, DeleteView):
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
