from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Tenant, TenantUser


class TenantAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = Tenant.objects.create(name='Acme Corporation')
        self.user = User.objects.create_user(username='tenantadmin', password='secret123')
        self.tenant_user = TenantUser.objects.create(
            user=self.user,
            tenant=self.tenant,
            role=TenantUser.ROLE_ADMIN,
            is_active=True,
        )

    def test_login_sets_tenant_id_in_session(self):
        response = self.client.post(
            reverse('tenant_login'),
            {'username': 'tenantadmin', 'password': 'secret123'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['tenant_id']), self.tenant.id)
        self.assertContains(response, 'Tenant: Acme Corporation')

    def test_logout_clears_tenant_session(self):
        self.client.login(username='tenantadmin', password='secret123')
        self.client.session['tenant_id'] = self.tenant.id
        self.client.session.save()

        response = self.client.post(reverse('tenant_logout'), follow=True)
        self.assertNotIn('tenant_id', self.client.session)
        self.assertContains(response, 'Login')

    def test_login_fails_for_user_without_tenant(self):
        user_without_tenant = User.objects.create_user(username='no_tenant', password='password')
        response = self.client.post(
            reverse('tenant_login'),
            {'username': 'no_tenant', 'password': 'password'},
            follow=True,
        )
        self.assertContains(response, 'Your account is not associated with an active tenant')
        self.assertNotIn('tenant_id', self.client.session)
