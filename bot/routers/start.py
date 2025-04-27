from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.keyboards import welcome_keyboard
from bot.functions import get_code, code_text

router = Router()


@router.message(CommandStart())
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    data = await get_code(telegram_id=telegram_id, first_name=first_name, last_name=last_name)

    if data["success"]:
        text = await code_text(data["code"])
        return await message.reply(
            text=text,
            reply_markup=welcome_keyboard()
        )
    else:
        text = data["message"]
        return await message.reply(
            text=text
        )
