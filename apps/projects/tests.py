from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.tenants.models import Tenant, TenantUser
from .models import Project


class ProjectViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Tenant One')
        self.other_tenant = Tenant.objects.create(name='Other Tenant')
        self.user = User.objects.create_user(username='adminuser', password='secret123')
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
        self.other_project = Project.objects.create(
            tenant=self.other_tenant,
            name='Other Project',
            description='A different tenant project.',
        )

    def login(self):
        self.client.login(username='adminuser', password='secret123')
        session = self.client.session
        session['tenant_id'] = self.tenant.id
        session.save()

    def test_project_list_is_tenant_scoped(self):
        self.login()
        response = self.client.get(reverse('project_list'))
        self.assertContains(response, 'Tenant Project')
        self.assertNotContains(response, 'Other Project')

    def test_project_create_sets_tenant(self):
        self.login()
        response = self.client.post(
            reverse('project_create'),
            {
                'name': 'New Tenant Project',
                'description': 'Created by tenant admin.',
                'status': Project.STATUS_PLANNED,
            },
            follow=True,
        )
        self.assertEqual(Project.objects.filter(tenant=self.tenant).count(), 2)
        self.assertContains(response, 'New Tenant Project')

    def test_project_detail_shows_metadata_and_tasks(self):
        self.login()
        response = self.client.get(reverse('project_detail', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tenant Project')
        self.assertContains(response, 'A project for the tenant.')
        self.assertContains(response, 'No tasks for this project yet.')

    def test_project_detail_is_tenant_scoped(self):
        self.login()
        response = self.client.get(reverse('project_detail', args=[self.other_project.pk]))
        self.assertEqual(response.status_code, 404)
