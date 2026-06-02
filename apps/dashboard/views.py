from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.common.decorators import tenant_required
from apps.projects.models import Project
from apps.tasks.models import Task


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    @method_decorator(tenant_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.tenant
        if tenant is None:
            context.update({
                'project_status_counts': {},
                'task_status_counts': {},
                'overdue_task_count': 0,
            })
            return context

        projects = Project.objects.filter(tenant=tenant)
        tasks = Task.objects.filter(tenant=tenant)

        project_status_counts = {
            item['status']: item['count']
            for item in projects.values('status').annotate(count=Count('id'))
        }
        task_status_counts = {
            item['status']: item['count']
            for item in tasks.values('status').annotate(count=Count('id'))
        }
        overdue_task_count = tasks.filter(
            due_date__lt=date.today(),
        ).exclude(status=Task.STATUS_DONE).count()

        context.update({
            'project_status_counts': project_status_counts,
            'task_status_counts': task_status_counts,
            'overdue_task_count': overdue_task_count,
        })
        return context
