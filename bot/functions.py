import random

from django.utils import timezone
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from apps.user.models import User, UserConfirmation


@sync_to_async
def get_code(telegram_id: int, first_name: str, last_name: str) -> dict:
    try:
        User.objects.get(telegram_id=telegram_id)
    except ObjectDoesNotExist:
        user = User(
            telegram_id=telegram_id,
            username=telegram_id,
            first_name=first_name,
            last_name=last_name,
            auth_type=User.AuthTypeChoices.telegram
        )

        user.save()

    code = random.randint(10000, 99999)

    try:
        confirmation = UserConfirmation.objects.get(telegram_id=telegram_id)
        if confirmation.expiration_time > timezone.now():
            return {
                "success": False,
                "message": "Eski kodingiz hali ham kuchda ☝️"
            }

        else:
            confirmation.delete()
            UserConfirmation.objects.create(
                telegram_id=telegram_id,
                code=code,
                expiration_time=timezone.now() + timezone.timedelta(minutes=2)
            )
    except ObjectDoesNotExist:
        UserConfirmation.objects.create(
            telegram_id=telegram_id,
            code=code,
            expiration_time=timezone.now() + timezone.timedelta(minutes=2)
        )

    return {
        "success": True,
        "code": code
    }


async def code_text(code: int) -> str:
    text = (f"🔒 Code: <code>{code}</code>\n"
            f"🔗 Click and Login: <code>https://google.com</code>")
    return text