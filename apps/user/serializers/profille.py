from rest_framework import serializers

from apps.user import models


class ProfileSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
            'telegram_id',
            'auth_type',
            'first_name',
            'last_name'
        )


class ProfileSerializerForPatch(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name'
        )