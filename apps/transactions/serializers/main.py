from rest_framework import serializers

from ..models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    operations_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'type',
            'icon',
            'operations_count'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({
            'user': user
        })

        return super().create(validated_data)

    @staticmethod
    def get_operations_count(obj):
        return obj.transactions.count()


class TransactionSerializerForGet(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    type = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'name',
            'type',
            'category',
            'amount',
            'comment',
            'created_at'
        )

    @staticmethod
    def get_type(obj):
        return obj.category.type


class TransactionSerializerForPostPatch(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'name',
            'amount',
            'category',
            'comment',
            'created_at'
        )


    def validate(self, attrs):
        category = attrs['category']

        if category.user != self.context['request'].user:
            raise serializers.ValidationError(detail={
                "error": "Bunday kategoriya sizda mavjud emas"
            })

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({
            'user': user
        })

        return super().create(validated_data)


