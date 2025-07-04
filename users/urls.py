from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ConfirmUserView, CustomTokenObtainPairView
from .oauth import GoogleLoginRedirectView, GoogleLoginCallbackView

urlpatterns = [
    # Existing URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('confirm/', ConfirmUserView.as_view(), name='confirm'),
    
    # Google OAuth URLs
    path('google-auth/', GoogleLoginRedirectView.as_view(), name='google-auth'),
    path('google-login/', GoogleLoginCallbackView.as_view(), name='google-login'),
    
    # Token URLs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]