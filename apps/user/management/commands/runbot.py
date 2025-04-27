import asyncio
import logging
import sys
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.routers import start_routers, get_code_routers
from core.security import SECURITY


class Command(BaseCommand):
    help = "Start the Telegram bot using Aiogram"

    def handle(self, *args, **kwargs):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        stream_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

        logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
        asyncio.run(self.start_bot())

    @staticmethod
    async def start_bot():
        bot = Bot(token=SECURITY.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        dp = Dispatcher()

        dp.include_router(start_routers)
        dp.include_router(get_code_routers)

        await dp.start_polling(bot)
