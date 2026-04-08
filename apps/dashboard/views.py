from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import CustomUser

@login_required
def dashboard_home(request):
    """Entry point for all user roles after login."""
    role = request.user.user_role
    if role == 'Customer':
        return redirect('customer_dashboard')
    elif role == 'Staff':
        return redirect('staff_dashboard')
    elif role in ['Unit', 'Admin', 'Super Admin']:
        return redirect('module_gateway')
    return redirect('landing')

@login_required
def customer_dashboard(request):
    page = request.GET.get('page', 'Profile')
    message = f"This is your personalized {page} overview."
    return render(request, 'dashboard/customer_dashboard.html', {'page': page, 'message': message})

@login_required
def staff_dashboard(request):
    page = request.GET.get('page', 'Daily Summary')
    message = f"View your {page} details."
    return render(request, 'dashboard/staff_dashboard.html', {'page': page, 'message': message})

@login_required
def module_gateway(request):
    """The central hub for administrative roles with secure entry steps."""
    module_slug = request.GET.get('module')
    
    # Instant Redirect for Super Admin
    if request.user.user_role == 'Super Admin' and module_slug:
        return redirect('module_dashboard', module_name=module_slug)
    
    step = request.GET.get('step', 'select')
    
    # Handle steps for module entry
    context = {
        'module_name': module_slug,
        'step': step,
    }
    
    if request.method == 'POST':
        if step == 'auth':
            # 1. Secondary Authentication (Double Login)
            password = request.POST.get('password')
            if request.user.check_password(password):
                return render(request, 'dashboard/module_gateway.html', {'module_name': module_slug, 'step': 'context'})
            else:
                messages.error(request, "Incorrect password. Secondary authentication failed.")
                return redirect('module_gateway')
        
        # 2. Handle Context selection in unified way
        if step == 'context':
            # Store selected context in session (Country/Unit)
            request.session['context_country'] = request.POST.get('context_country')
            request.session['context_unit'] = request.POST.get('context_unit')
            return redirect('module_dashboard', module_name=module_slug)
            
    return render(request, 'dashboard/module_gateway.html', context)

@login_required
def module_dashboard(request, module_name):
    """Router to departmental dashboards after gateway validation."""
    # Match module names to their app-specific dashboard URLs
    app_urls = {
        'attendance': 'attendance_dashboard',
        'order': 'orders_dashboard',
        'hr': 'hr_dashboard',
        'incident': 'incidents_dashboard',
        'equipment': 'equipment_dashboard',
    }
    target_url = app_urls.get(module_name)
    if target_url:
        return redirect(target_url)
    return redirect('dashboard_home')
