from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_refresh_token = None

        if header is None:
            raw_access_token = request.COOKIES.get('access_token')
            raw_refresh_token = request.COOKIES.get('refresh_token')
        else:
            raw_access_token = self.get_raw_token(header)

        try:
            validated_token = self.get_validated_token(raw_access_token)
            user = self.get_user(validated_token)
            return user, validated_token
        except Exception:
            if raw_refresh_token:
                try:
                    refresh_token = RefreshToken(raw_refresh_token)
                    new_access_token = str(refresh_token.access_token)

                    response = Response()
                    response.set_cookie(
                        key="access_token",
                        value=new_access_token,
                        httponly=True,
                        secure=True,
                        samesite="Lax",
                        max_age=60 * 60 * 24,
                    )
                    return self.get_user(refresh_token), refresh_token
                except Exception:
                    return None

            return None
