from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.projects.models import Project
from apps.tenants.models import Tenant, TenantUser
from apps.tasks.models import Task


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Tenant A')
        self.other_tenant = Tenant.objects.create(name='Tenant B')
        self.user = User.objects.create_user(username='dashboarduser', password='secret123')
        self.tenant_user = TenantUser.objects.create(
            user=self.user,
            tenant=self.tenant,
            role=TenantUser.ROLE_ADMIN,
            is_active=True,
        )
        self.project_planned = Project.objects.create(
            tenant=self.tenant,
            name='Planned Project',
            description='Planned',
            status=Project.STATUS_PLANNED,
        )
        self.project_active = Project.objects.create(
            tenant=self.tenant,
            name='Active Project',
            description='Active',
            status=Project.STATUS_ACTIVE,
        )
        self.task_todo = Task.objects.create(
            tenant=self.tenant,
            project=self.project_planned,
            title='To Do Task',
            status=Task.STATUS_TODO,
            due_date=date.today() - timedelta(days=1),
        )
        self.task_done = Task.objects.create(
            tenant=self.tenant,
            project=self.project_active,
            title='Done Task',
            status=Task.STATUS_DONE,
            due_date=date.today() - timedelta(days=3),
        )
        self.other_task = Task.objects.create(
            tenant=self.other_tenant,
            project=Project.objects.create(
                tenant=self.other_tenant,
                name='Other',
                description='Other',
            ),
            title='Other Task',
            status=Task.STATUS_TODO,
            due_date=date.today() - timedelta(days=2),
        )

    def login(self):
        self.client.login(username='dashboarduser', password='secret123')
        session = self.client.session
        session['tenant_id'] = self.tenant.id
        session.save()

    def test_dashboard_counts(self):
        self.login()
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projects by Status')
        self.assertContains(response, 'PLANNED: 1')
        self.assertContains(response, 'ACTIVE: 1')
        self.assertContains(response, 'Tasks by Status')
        self.assertContains(response, 'TODO: 1')
        self.assertContains(response, 'DONE: 1')
        self.assertContains(response, 'Overdue Tasks')
        self.assertContains(response, '1')

    def test_dashboard_is_tenant_scoped(self):
        self.login()
        response = self.client.get(reverse('dashboard_home'))
        self.assertNotContains(response, 'Other Task')
