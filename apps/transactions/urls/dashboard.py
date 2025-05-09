from django.urls import path
from apps.transactions.views import dashboard as views


urlpatterns = [
    path('category-chart/', views.CategoryChartView.as_view())
]