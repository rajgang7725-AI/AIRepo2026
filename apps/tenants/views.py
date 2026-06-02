from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import TenantAuthenticationForm


class TenantLoginView(LoginView):
    template_name = 'tenants/login.html'
    authentication_form = TenantAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        tenant_user = getattr(user, 'tenantuser', None)
        if tenant_user is not None:
            self.request.session['tenant_id'] = tenant_user.tenant_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tenant_home')


class TenantLogoutView(LogoutView):
    next_page = reverse_lazy('tenant_login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.session.pop('tenant_id', None)
        return response


def home(request):
    return render(request, 'tenants/home.html')
