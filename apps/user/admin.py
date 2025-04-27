from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.user import models
from django.contrib.auth.models import Group

# Register your models here.
admin.site.unregister(Group)


@admin.register(models.User)
class UserAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'telegram_id', 'is_verified', 'auth_type', 'username')


@admin.register(models.UserConfirmation)
class UserConfirmationAdmin(ModelAdmin):
    list_display = ('telegram_id', 'code', 'expiration_time', 'times')