from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.transactions import serializers
from apps.transactions.models import Category, Transaction


# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('post', 'patch', 'get', 'delete')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated, )
    http_method_names = ('post', 'patch', 'get', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TransactionSerializerForGet
        return serializers.TransactionSerializerForPostPatch

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

