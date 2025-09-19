import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from .config import cfg
from .db import init_db
from .handlers import common as common_handlers
from .handlers import reflection as reflection_handlers
from .handlers import practices as practices_handlers

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(reflection_handlers.router)
    dp.include_router(practices_handlers.router)
    dp.include_router(common_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
