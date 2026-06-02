from apps.tenants.models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        request.tenant_user = None
        tenant_id = request.session.get('tenant_id')

        if request.user.is_authenticated:
            tenant_user = getattr(request.user, 'tenantuser', None)
            if tenant_user and tenant_user.is_active:
                request.tenant_user = tenant_user
                if tenant_id != tenant_user.tenant_id:
                    tenant_id = tenant_user.tenant_id
                    request.session['tenant_id'] = tenant_id

        if tenant_id:
            try:
                request.tenant = Tenant.objects.get(id=tenant_id)
            except Tenant.DoesNotExist:
                request.session.pop('tenant_id', None)
                request.tenant = None

        return self.get_response(request)
