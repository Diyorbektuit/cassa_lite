from django.urls import path

from apps.user.views import profile as views

urlpatterns = [
    path('', views.ProfileView.as_view())
]