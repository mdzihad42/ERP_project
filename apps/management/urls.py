from django.urls import path
from .views import (
    admin_unit_list, admin_unit_create, admin_unit_edit,
    admin_department_list, admin_department_create, admin_department_edit,
    admin_position_list, admin_position_create, admin_position_edit,
    admin_delete
)

urlpatterns = [
    # Unit Management
    path('admin/unit/', admin_unit_list, name='admin_unit'),
    path('admin/unit/create/', admin_unit_create, name='admin_unit_create'),
    path('admin/unit/edit/<int:pk>/', admin_unit_edit, name='admin_unit_edit'),
    path('admin/unit/delete/<int:pk>/', admin_delete, {'model_name': 'unit'}, name='admin_unit_delete'),

    # Department Management
    path('admin/department/', admin_department_list, name='admin_department'),
    path('admin/department/create/', admin_department_create, name='admin_department_create'),
    path('admin/department/edit/<int:pk>/', admin_department_edit, name='admin_department_edit'),
    path('admin/department/delete/<int:pk>/', admin_delete, {'model_name': 'department'}, name='admin_department_delete'),

    # Position Management
    path('admin/position/', admin_position_list, name='admin_position'),
    path('admin/position/create/', admin_position_create, name='admin_position_create'),
    path('admin/position/edit/<int:pk>/', admin_position_edit, name='admin_position_edit'),
    path('admin/position/delete/<int:pk>/', admin_delete, {'model_name': 'position'}, name='admin_position_delete'),
]
