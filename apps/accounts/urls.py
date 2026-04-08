from django.urls import path
from .views import (
    unified_auth, login_view, register_view, verify_otp, 
    forgot_password_view, logout_view, 
    user_approval, approve_user, admin_permissions, admin_track
)

urlpatterns = [
    path('', unified_auth, name='accounts_auth'),
    path('login/', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('logout/', logout_view, name='logout'),
    
    # Super Admin: User Permission Module
    path('admin/approvals/', user_approval, name='user_approval'),
    path('admin/approvals/approve/<int:user_id>/', approve_user, name='approve_user'),
    path('admin/permissions/', admin_permissions, name='admin_permissions'),
    path('admin/track/', admin_track, name='admin_track'),
]
