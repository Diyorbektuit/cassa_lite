from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.transactions import models


# Register your models here.
@admin.register(models.Category)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'user', 'type', 'name')


@admin.register(models.Transaction)
class UserConfirmationAdmin(ModelAdmin):
    list_display = ('id', 'user', 'category', 'amount')