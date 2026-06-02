from django import forms
from django.contrib.auth.forms import AuthenticationForm


class TenantAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        tenant_user = getattr(user, 'tenantuser', None)
        if tenant_user is None:
            raise forms.ValidationError(
                'Your account is not associated with an active tenant. Contact your administrator.',
                code='no_tenant_user',
            )
        if not tenant_user.is_active:
            raise forms.ValidationError(
                'Your tenant user account is inactive. Contact your administrator.',
                code='inactive_tenant_user',
            )
