from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from apps.management.models import Country, State, City, UnitNumber, Department, Position

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_role', 'Super Admin')
        extra_fields.setdefault('status', 'Approved')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Staff', 'Staff'),
        ('Unit', 'Unit'),
        ('Admin', 'Admin'),
        ('Super Admin', 'Super Admin'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Required Basic Fields
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    
    # Selection Fields
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Location Hierarchy
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Employee Specific Fields
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    unit_no = models.ForeignKey(UnitNumber, on_delete=models.SET_NULL, null=True, blank=True)

    # Django Internal Fields
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True) # Profile is active but "Approved" status gate keeps them out
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) - {self.user_role}"

class OTPVerification(models.Model):
    user_email = models.EmailField() # Use email directly to verify before User is created
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    purpose = models.CharField(max_length=20, choices=[('Register', 'Register'), ('Login', 'Login'), ('Forgot', 'Forgot')], default='Register')

    def is_expired(self):
        # 5 minutes expiration
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

class UserLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=255) # e.g. "Logged In", "Created Order", "Deleted User"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Context fields for filtering as requested
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    unit_no = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
