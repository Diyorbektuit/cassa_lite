from django.urls import path
from apps.user.views import auth as views


urlpatterns = [
    path('google/auth/', views.GoogleAuthView.as_view()),
    path('google/callback/', views.GoogleCallbackView.as_view()),

    path('telegram/verify/', views.UserTelegramVerifyView.as_view())
]