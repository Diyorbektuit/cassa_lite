from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.transactions.serializers import dashboard as serializers
from apps.transactions.models import Category, Transaction


class CategoryChartView(generics.ListAPIView):
    serializer_class = serializers.CategoryChartSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return user.categories.all()