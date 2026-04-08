from django.contrib import admin
from django.urls import path, include
from apps.common.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    
    # Auth & Account Management
    path('accounts/', include('apps.accounts.urls')),
    
    # Global Management (CRUD for Units, Depts, etc.)
    path('management/', include('apps.management.urls')),
    
    # Dashboard Gateway & Role-based Hubs
    path('dashboard/', include('apps.dashboard.urls')),
    
    # Department-Specific Modules
    path('attendance/', include('apps.attendance.urls')),
    path('orders/', include('apps.orders.urls')),
    path('hr/', include('apps.hr.urls')),
    path('incidents/', include('apps.incidents.urls')),
    path('equipment/', include('apps.equipment.urls')),
]