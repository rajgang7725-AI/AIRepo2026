from functools import wraps
from django.http import HttpResponseForbidden


def tenant_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.tenant:
            return HttpResponseForbidden('Tenant context required.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated or not hasattr(user, 'tenantuser'):
                return HttpResponseForbidden('Role required.')
            if request.tenant is None or user.tenantuser.tenant_id != request.tenant.id:
                return HttpResponseForbidden('Tenant mismatch.')
            if user.tenantuser.role not in roles:
                return HttpResponseForbidden('Insufficient role.')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
