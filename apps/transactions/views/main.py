from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.transactions.serializers import main as serializers
from apps.transactions.models import Category, Transaction
from ..filters import TransactionFilter


# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAuthenticated, )
    search_fields = ('name',)
    http_method_names = ('post', 'patch', 'get', 'delete')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated, )
    http_method_names = ('post', 'patch', 'get', 'delete')
    search_fields = ('name', )
    filterset_class = TransactionFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter with attraction category idmulti",
                type=openapi.FORMAT_UUID
            ),
            openapi.Parameter(
                'min_price',
                openapi.IN_QUERY,
                description="minimum price for tariffs",
                type=openapi.FORMAT_INT64
            ),
            openapi.Parameter(
                'max_price',
                openapi.IN_QUERY,
                description="maximum price for tariffs",
                type=openapi.FORMAT_INT64
            )
        ]
    )
    def list(self, *args, **kwargs):
        return super().list(args, kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TransactionSerializerForGet
        return serializers.TransactionSerializerForPostPatch

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

