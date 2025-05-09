from django.db.models import Sum
from rest_framework import serializers

from ..models import Category, Transaction


class CategoryChartSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'category_name',
            'percentage'
        )

    def get_percentage(self, obj) -> int:
        user = self.context['request'].user
        if user.transactions is None or obj.transactions is None:
            return 0
        else:
            all_amount = user.transactions.aggregate(
                all_amount=Sum('amount')
            )['all_amount']
            category_amount = obj.transactions.aggregate(
                all_amount=Sum('amount')
            )['all_amount']

            percentage: int = (category_amount / all_amount) * 100
            return percentage

