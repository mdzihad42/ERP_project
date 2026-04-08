from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import CustomUser, OTPVerification, UserLog
from .forms import LoginForm, RegisterForm
from .utils import generate_otp, send_otp_email

# --- Unified Auth View ---
def unified_auth(request):
    role = request.GET.get('role', 'customer')
    active_tab = request.GET.get('tab', 'login')
    
    role_labels = {
        'customer': 'Customer',
        'staff': 'Staff',
        'unit': 'Unit',
        'admin': 'Admin',
        'super_admin': 'Super Admin'
    }
    
    context = {
        'role': role,
        'role_label': role_labels.get(role, 'User'),
        'active_tab': active_tab,
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
    }
    return render(request, 'accounts/auth.html', context)

# --- Login Logic ---
def login_view(request):
    role = request.GET.get('role', 'customer')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # 1. Preliminary Authentication
            user = authenticate(request, email=email, password=password)
            if user:
                # 2. Check Approval Status
                if user.status != 'Approved':
                    messages.error(request, "Approval Pending. Please wait for Super Admin approval.")
                    return redirect(f'/accounts/?role={role}&tab=login')
                
                # 3. Generate and Send OTP
                otp_code = generate_otp()
                OTPVerification.objects.create(user_email=email, otp_code=otp_code, purpose='Login')
                send_otp_email(email, otp_code, purpose='Login')
                
                # 4. Redirect to OTP verification
                return render(request, 'accounts/verify.html', {'email': email, 'purpose': 'Login', 'role': role})
            else:
                messages.error(request, "Invalid credentials or account not found.")
                return redirect(f'/accounts/?role={role}&tab=login')
    return redirect('landing')

# --- Register Logic ---
def register_view(request):
    role = request.GET.get('role', 'customer')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Temporary Save (Data kept in session until OTP verified)
            request.session['reg_data'] = request.POST # Save all fields to recreate user on OTP success
            
            # 1. Generate and Send OTP
            otp_code = generate_otp()
            OTPVerification.objects.create(user_email=email, otp_code=otp_code, purpose='Register')
            send_otp_email(email, otp_code, purpose='Register')
            
            return render(request, 'accounts/verify.html', {'email': email, 'purpose': 'Register', 'role': role})
        else:
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'accounts/auth.html', {'role': role, 'register_form': form, 'active_tab': 'register', 'login_form': LoginForm()})
    return redirect('landing')

# --- OTP Verification Logic ---
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        purpose = request.POST.get('purpose')
        role = request.POST.get('role')
        
        # 1. Check database for valid OTP
        otp_record = OTPVerification.objects.filter(user_email=email, otp_code=otp, purpose=purpose).last()
        
        if otp_record and not otp_record.is_expired():
            otp_record.is_verified = True
            otp_record.save()
            
            if purpose == 'Login':
                user = CustomUser.objects.get(email=email)
                login(request, user)
                # Redirect to relevant dashboard based on role
                return redirect('dashboard_home') # Role-aware redirection hub
            
            elif purpose == 'Register':
                reg_data = request.session.get('reg_data')
                if reg_data:
                    # Re-instantiate registration form to save correctly
                    form = RegisterForm(reg_data)
                    if form.is_valid():
                        user = form.save(commit=False)
                        user.set_password(reg_data['password'])
                        user.user_role = role.capitalize() # Match choices
                        user.status = 'Pending' # Always pending initially
                        user.save()
                        messages.success(request, "Registration successful! Please wait for Super Admin approval.")
                        return redirect('landing')
            
            elif purpose == 'Forgot':
                messages.success(request, "OTP Verified. Update your password.")
                return render(request, 'accounts/forgot.html', {'email': email, 'otp_verified': True})

        else:
            messages.error(request, "Invalid or expired OTP code.")
            return render(request, 'accounts/verify.html', {'email': email, 'purpose': purpose, 'role': role})
    
    return redirect('landing')

# --- Forgot Password Logic ---
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = generate_otp()
        OTPVerification.objects.create(user_email=email, otp_code=otp_code, purpose='Forgot')
        send_otp_email(email, otp_code, purpose='Forgot')
        return render(request, 'accounts/verify.html', {'email': email, 'purpose': 'Forgot'})
    return render(request, 'accounts/forgot.html')

# --- Super Admin: User Approval ---
def user_approval(request):
    pending_users = CustomUser.objects.filter(status='Pending').order_by('-date_joined')
    return render(request, 'accounts/admin/user_approval.html', {'pending_users': pending_users})

def approve_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        action = request.POST.get('action')
        if action == 'approve':
            user.status = 'Approved'
            user.save()
            messages.success(request, f"User {user.email} has been approved.")
        elif action == 'reject':
            user.delete()
            messages.warning(request, f"User registration for {user.email} was rejected and deleted.")
    return redirect('user_approval')

# --- Super Admin: User Permissions ---
def admin_permissions(request):
    users = CustomUser.objects.all().select_related('unit_no', 'country')
    return render(request, 'accounts/admin/user_permissions.html', {'users': users})

# --- Super Admin: User Track ---
def admin_track(request):
    logs = UserLog.objects.all().select_related('user').order_by('-timestamp')
    # Basic filtering logic can be added here
    return render(request, 'accounts/admin/user_track.html', {'logs': logs})

# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('landing')
