from django.db import models

from apps.globals.models import BaseModel
from apps.user.models import User

# Create your models here.
class Category(BaseModel):
    class TypeChoice(models.TextChoices):
        income = 'income'
        expense = 'expense'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    type = models.CharField(max_length=20, choices=TypeChoice.choices)
    name = models.CharField(max_length=256)
    icon = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.name}"


class Transaction(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    amount = models.PositiveIntegerField()
    name = models.CharField(max_length=512)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.name} | {self.amount} | {self.user}"