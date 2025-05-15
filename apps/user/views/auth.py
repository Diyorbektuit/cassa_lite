import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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

        # 1. Google Token olish
        token_url = "https://accounts.google.com/o/oauth2/token"
        token_payload = {
            "code": code,
            "client_id": SECURITY.GOOGLE_CLIENT_ID,
            "client_secret": SECURITY.GOOGLE_CLIENT_SECRET,
            "redirect_uri": SECURITY.google_redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(token_url, data=token_payload)

        if response.status_code != 200:
            return Response({"error": "Invalid token request"}, status=response.status_code)

        access_token = response.json().get("access_token")

        user_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_response = requests.get(
            user_url, headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=user_response.status_code)

        user_data = user_response.json()

        info = user_create_or_update(user_data)

        access = info.get("access_token")
        refresh = info.get("refresh_token")

        response = HttpResponse()

        if request.is_secure():
            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 10,  # 10 kun
                domain=".kassalite.uz"
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 30,  # 30 kun
                domain=".kassalite.uz"
            )
        else:
            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 10,  # 10 kun
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 30,  # 30 kun
            )
        response.status_code = 302
        response["Location"] = f"{SECURITY.redirect_url}"

        return response


class UserTelegramVerifyView(APIView):

    @swagger_auto_schema(request_body=serializers.TelegramVerifySerializer)
    def post(self, args, **kwargs):
        verify_serializer = serializers.TelegramVerifySerializer(data=self.request.data)

        if verify_serializer.is_valid():
            user = verify_serializer.create(verify_serializer.validated_data)
            access = verify_serializer.to_representation(user).get("access_token")
            refresh = verify_serializer.to_representation(user).get("refresh_token")
            response = Response(data=verify_serializer.to_representation(user))
            if self.request.is_secure():
                response.set_cookie(
                    key="access_token",
                    value=str(access),
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 10,  # 10 kun
                    domain=".kassalite.uz"
                )
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 30,  # 30 kun
                    domain=".kassalite.uz"
                )
            else:
                response.set_cookie(
                    key="access_token",
                    value=str(access),
                    httponly=True,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 10,  # 10 kun
                )
                response.set_cookie(
                    key="refresh_token",
                    value=str(refresh),
                    httponly=True,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 30,  # 30 kun
                )
            return response
        else:
            return Response(data=verify_serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, *args, **kwargs):
        request = self.request
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        if self.request.is_secure():
            response.delete_cookie('access_token', domain=".kassalite.uz")
            response.delete_cookie('refresh_token', domain=".kassalite.uz")

        return response
