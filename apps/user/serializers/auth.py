from rest_framework import serializers
from django.utils import timezone

from ..models import UserConfirmation, User


class TelegramVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)

    def validate(self, attrs):
        code = attrs.get('code')

        if UserConfirmation.objects.filter(code=code, expiration_time__gte=timezone.now()):
            confirmation = UserConfirmation.objects.filter(code=code, expiration_time__gte=timezone.now()).first()
            telegram_id = confirmation.telegram_id
            confirmation.delete()
        else:
            raise serializers.ValidationError(detail={
                "error": "Kod xato yoki allaqachon eskirgan"
            })

        attrs['telegram_id'] = telegram_id
        return attrs

    def create(self, validated_data):
        telegram_id = validated_data.get('telegram_id')

        user = User.objects.get(telegram_id=telegram_id)
        user.is_verified = True
        user.save()

        return user

    def to_representation(self, instance):
        return {
            "success": True,
        }


