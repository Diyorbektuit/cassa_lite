import requests
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.utils import user_create_or_update
from core.security import SECURITY
from apps.user.serializers import auth as serializers


# Google Auth
class GoogleAuthView(APIView):

    def get(self, *args, **kwargs):

        google_oauth_url = "https://accounts.google.com/o/oauth2/auth"
        scope = "openid profile email"
        google_auth_url = (f"{google_oauth_url}?client_id={SECURITY.GOOGLE_CLIENT_ID}&"
                           f"redirect_uri={SECURITY.google_redirect_uri}"
                           f"&scope={scope}&response_type=code&")

        return redirect(google_auth_url)


# Google Callback
class GoogleCallbackView(APIView):
    schema = None

    def get(self, request):
        code = request.GET.get("code")

        token_url = "https://accounts.google.com/o/oauth2/token"
        token_payload = {
            "code": code,
            "client_id": SECURITY.GOOGLE_CLIENT_ID,
            "client_secret": SECURITY.GOOGLE_CLIENT_SECRET,
            "redirect_uri": SECURITY.google_redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=token_payload)


        access_token = response.json().get("access_token")
        if response.status_code != 200:
            return Response({"error": "Invalid token request"}, status=response.status_code)

        user_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_response = requests.get(
            user_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        info = user_create_or_update(user_response.json())
        return redirect(f"{SECURITY.redirect_url}?access={info.get('access_token')}&refresh={info.get('refresh_token')}")


class UserTelegramVerifyView(APIView):

    @swagger_auto_schema(request_body=serializers.TelegramVerifySerializer)
    def post(self, args, **kwargs):
        verify_serializer = serializers.TelegramVerifySerializer(data=self.request.data)

        if verify_serializer.is_valid():
            user = verify_serializer.create(verify_serializer.validated_data)
            return Response(data=verify_serializer.to_representation(user))
        else:
            return Response(data=verify_serializer.errors, status=400)
