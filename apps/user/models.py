from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager

from apps.globals.models import BaseModel


class UserManager(AbstractUserManager):
    def _create_user(self, password, email=None, telegram_id=None, username=None, **extra_fields):
        if email is not None:
            user = self.model(email=email, username=email, **extra_fields)
        elif telegram_id is not None:
            user = self.model(email=email, username=telegram_id, **extra_fields)
        elif username is not None:
            user = self.model(username=username, **extra_fields)
        else:
            raise ValueError("The given email or phone_number must be set")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('auth_type', 'google')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email=f"{username}@kassalite.uz", username=username, password=password, **extra_fields)

    def create_user(self, email=None, telegram_id=None, password=None, **extra_fields):
        if password is None:
            password = str(uuid4())
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("auth_type", "via_email")

        return self._create_user(email=email, telegram_id=telegram_id, password=password, **extra_fields)


class User(AbstractUser, BaseModel):
    REQUIRED_FIELDS = []

    class AuthTypeChoices(models.TextChoices):
        telegram = 'telegram'
        google = 'google'

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=20, choices=AuthTypeChoices.choices, null=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.password = uuid4()
            if not self.username and self.email:
                self.username = self.email
            elif not self.username and self.telegram_id:
                self.username = self.telegram_id
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserConfirmation(BaseModel):
    code = models.BigIntegerField(null=False)
    expiration_time = models.DateTimeField()
    telegram_id = models.CharField(max_length=255, blank=True, null=True)
    times = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"Confirmation for {self.telegram_id}"