from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import random
import string
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


def generate_confirmation_code(length=6):
    return ''.join(random.choices(string.digits, k=length)) 

# Add these views for Google OAuth
class GoogleLoginRedirectView(APIView):
    def get(self, request):
        """Redirect user to Google OAuth consent screen"""
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = "http://localhost:8000/api/v1/users/google-login"
        
        import urllib.parse
        encoded_redirect = urllib.parse.quote_plus(redirect_uri)
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={encoded_redirect}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        return redirect(auth_url)

class GoogleLoginCallbackView(APIView):
    def get(self, request):
        """Handle the OAuth callback from Google"""
        code = request.GET.get('code')
        if not code:
            return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        redirect_uri = "http://localhost:8000/api/v1/users/google-login"
        
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=data)
        if not token_response.ok:
            return Response({"error": "Failed to get token"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        # Get user info using v3 endpoint as suggested
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)
        
        if not user_info_response.ok:
            return Response({"error": "Failed to get user info"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = user_info_response.json()
        
        # Get or create user
        email = user_info.get('email')
        if not email:
            return Response({"error": "Email not provided by Google"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]  # Simple username from email
            user = User.objects.create_user(
                email=email,
                username=username,
                is_active=True  # Google users are pre-verified
            )
            # Optionally set more user data
            if 'given_name' in user_info:
                user.first_name = user_info['given_name']
            if 'family_name' in user_info:
                user.last_name = user_info['family_name']
            user.save()

            confirmation_code = generate_confirmation_code()
            cache.set(f"confirm_code_{user.id}", confirmation_code, timeout=300)

            # Use Celery task to send OTP email asynchronously
            from .tasks import send_otp_email
            send_otp_email.delay(user.id, confirmation_code)

            return Response({
                "message": "User registered. Confirmation code sent to your email.",
                "user_id": user.id,
                "expires_in": "5 minutes"
            }, status=status.HTTP_201_CREATED)


        # For existing users, check if they're active
        if not user.is_active:
            # Get confirmation code from Redis
            confirmation_code = cache.get(f"confirm_code_{user.id}")
            if not confirmation_code:
                # Generate a new code if expired
                confirmation_code = generate_confirmation_code()
                cache.set(f"confirm_code_{user.id}", confirmation_code, timeout=300)
                
                # Use Celery task to send OTP email asynchronously
                from .tasks import send_otp_email
                send_otp_email.delay(user.id, confirmation_code)
                
                return Response({
                    "message": "User needs confirmation. New code sent to your email.",
                    "user_id": user.id,
                    "expires_in": "5 minutes"
                })
            else:
                return Response({
                    "message": "User needs confirmation. Check your email for the code.",
                    "user_id": user.id
                })
       
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'username': user.username,
                'is_active': user.is_active
            }
        })
        
class ConfirmUserView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        code = request.data.get('code')
        
        if not user_id or not code:
            return Response({"error": "User ID and confirmation code required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the code from Redis
        stored_code = cache.get(f"confirm_code_{user_id}")
        
        if not stored_code:
            return Response({"error": "Confirmation code expired"}, status=status.HTTP_400_BAD_REQUEST)
            
        if code != stored_code:
            return Response({"error": "Invalid confirmation code"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Activate the user
        user.is_active = True
        user.save()
        
        # Delete the code from Redis
        cache.delete(f"confirm_code_{user_id}")
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "User confirmed successfully",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })