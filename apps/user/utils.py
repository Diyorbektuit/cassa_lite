from .models import User


def user_create_or_update(data: dict) -> dict:
    print(data)
    first_name = data.get('given_name')
    last_name = data.get('family_name')
    email = data.get('email')

    users = User.objects.filter(email=email)
    if users.exists():
        user = users.first()
    else:
        user = User(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name,
            auth_type=User.AuthTypeChoices.google
        )


    user.is_verified = True
    user.save()

    return {
        "success": True,
        "access_token": user.tokens()["access"],
        "refresh_token": user.tokens()["refresh"],
    }