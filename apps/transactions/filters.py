import django_filters
from apps.transactions.models import Transaction

class IntegerInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class TransactionFilter(django_filters.FilterSet):
    category = IntegerInFilter(field_name="category__id", lookup_expr="in")
    min_price = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ["category", "min_price", "max_price"]
