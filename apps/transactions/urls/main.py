from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.transactions.views.main import CategoryViewSet, TransactionViewSet

router = DefaultRouter()

router.register(prefix='category', viewset=CategoryViewSet)
router.register(prefix='transaction', viewset=TransactionViewSet)


urlpatterns = [
    path('', include(router.urls))
]