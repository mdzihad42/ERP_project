import random
from django.core.mail import send_mail
from .models import OTPVerification

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp_code, purpose="verification"):
    subject = f"Your Bavaria ERP OTP Code for {purpose}"
    message = f"Your 6-digit OTP code is: {otp_code}. This code will expire in 5 minutes."
    try:
        # Configuration for console backend (settings.py)
        # Note: In production replace with real SMTP backend
        send_mail(subject, message, 'support@bavariaerp.com', [email])
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
