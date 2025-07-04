from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@shared_task
def send_otp_email(user_id, otp_code):
    """
    Send OTP code to user's email for verification
    """
    try:
        user = User.objects.get(id=user_id)
        subject = 'Your OTP Verification Code'
        message = f'Hello {user.username},\n\nYour OTP verification code is: {otp_code}\n\nThis code will expire in 5 minutes.\n\nBest regards,\nThe Shop API Team'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return f"OTP email sent to {user.email}"
    except User.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as e:
        return f"Failed to send OTP email: {str(e)}"

@shared_task
def send_hourly_greeting():
    """
    Send hourly greeting emails to all active users
    """
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        subject = 'Hourly Greeting from Shop API'
        message = f'Hello {user.username},\n\nWe hope you are having a great day! Thank you for being part of our community.\n\nBest regards,\nThe Shop API Team'
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send hourly greeting to {user.email}: {str(e)}")
    
    return f"Hourly greetings sent to {active_users.count()} users"