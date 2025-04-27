from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def welcome_keyboard() -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(
        text="Yangilash",
        callback_data="renew"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button1]
        ]
    )

    return keyboard