from aiogram import Router, types, F
from bot.functions import get_code, code_text
from bot.keyboards import welcome_keyboard

router = Router()

@router.callback_query(F.data == "renew")
async def renew_callback(query: types.CallbackQuery):
    telegram_id = query.from_user.id
    first_name = query.from_user.first_name
    last_name = query.from_user.last_name
    data = await get_code(telegram_id=telegram_id, first_name=first_name, last_name=last_name)

    if data["success"]:
        text = await code_text(data["code"])
        return await query.message.edit_text(
            text=text,
            reply_markup=welcome_keyboard()
        )
    else:
        text = data["message"]
        return await query.message.reply(
            text=text
        )


