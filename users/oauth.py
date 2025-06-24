import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return Response({'error': 'No code provided'}, status=400)

        # Exchange code for token
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': 'http://localhost:8000/api/v1/users/google-login',
            'grant_type': 'authorization_code',
        }
        token_resp = requests.post(token_url, data=data)
        token_json = token_resp.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response({'error': 'Failed to get access token', 'details': token_json}, status=400)

        # Get user info from v3 endpoint
        userinfo_resp = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo = userinfo_resp.json()
        return Response(userinfo)