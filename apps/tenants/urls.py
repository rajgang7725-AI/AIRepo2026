from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tenant_home'),
    path('login/', views.TenantLoginView.as_view(), name='tenant_login'),
    path('logout/', views.TenantLogoutView.as_view(), name='tenant_logout'),
]
