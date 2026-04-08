from django.urls import path
from .views import dashboard_home, customer_dashboard, staff_dashboard, module_gateway, module_dashboard

urlpatterns = [
    path('home/', dashboard_home, name='dashboard_home'),
    path('customer/', customer_dashboard, name='customer_dashboard'),
    path('staff/', staff_dashboard, name='staff_dashboard'),
    path('gateway/', module_gateway, name='module_gateway'),
    path('module/<slug:module_name>/', module_dashboard, name='module_dashboard'),
]
