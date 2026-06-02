from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.projects.models import Project
from apps.tenants.models import Tenant, TenantUser
from .models import Task


class TaskViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Tenant One')
        self.other_tenant = Tenant.objects.create(name='Other Tenant')
        self.user = User.objects.create_user(username='taskadmin', password='secret123')
        self.tenant_user = TenantUser.objects.create(
            user=self.user,
            tenant=self.tenant,
            role=TenantUser.ROLE_ADMIN,
            is_active=True,
        )
        self.project = Project.objects.create(
            tenant=self.tenant,
            name='Tenant Project',
            description='A project for the tenant.',
        )
        self.task = Task.objects.create(
            tenant=self.tenant,
            project=self.project,
            title='Tenant Task',
            description='A task for this tenant.',
            status=Task.STATUS_TODO,
        )

    def login(self):
        self.client.login(username='taskadmin', password='secret123')
        session = self.client.session
        session['tenant_id'] = self.tenant.id
        session.save()

    def test_task_list_is_tenant_scoped(self):
        self.login()
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Tenant Task')

    def test_task_create_sets_tenant(self):
        self.login()
        response = self.client.post(
            reverse('task_create'),
            {
                'project': self.project.id,
                'title': 'New Tenant Task',
                'description': 'Created through task create.',
                'status': Task.STATUS_TODO,
            },
            follow=True,
        )
        self.assertEqual(Task.objects.filter(tenant=self.tenant).count(), 2)
        self.assertContains(response, 'New Tenant Task')

    def test_task_detail_shows_metadata_and_effort(self):
        self.task.estimated_hours = 8
        self.task.actual_hours = 5
        self.task.save()

        self.login()
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tenant Task')
        self.assertContains(response, 'A task for this tenant.')
        self.assertContains(response, 'Estimated hours: 8')
        self.assertContains(response, 'Actual hours: 5')

    def test_task_detail_is_tenant_scoped(self):
        other_project = Project.objects.create(
            tenant=self.other_tenant,
            name='Other Tenant Project',
            description='Other project',
        )
        other_task = Task.objects.create(
            tenant=self.other_tenant,
            project=other_project,
            title='Other Task',
            description='Other tenant task.',
            status=Task.STATUS_TODO,
        )

        self.login()
        response = self.client.get(reverse('task_detail', args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)
