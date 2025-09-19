#!/usr/bin/env python3
"""
Локальный сервер для тестирования бота
"""

import asyncio
import logging
from aiohttp import web
import json
import sys
import os

# Добавляем путь к приложению
sys.path.append(os.path.dirname(__file__))

from app.config import cfg
from app.db import init_db
from app.handlers import common as common_handlers
from app.handlers import reflection as reflection_handlers
from app.handlers import practices as practices_handlers

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Регистрация обработчиков
dp.include_router(reflection_handlers.router)
dp.include_router(practices_handlers.router)
dp.include_router(common_handlers.router)

async def webhook_handler(request):
    """Обработчик webhook"""
    try:
        # Читаем данные
        data = await request.json()
        
        # Создаем объект Update
        update = Update(**data)
        
        # Обрабатываем обновление
        await dp.feed_update(bot, update)
        
        return web.json_response({"ok": True})
        
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        return web.json_response({"ok": False, "error": str(e)}, status=500)

async def health_check(request):
    """Проверка здоровья сервера"""
    return web.Response(text="Bot is running!")

async def init_app():
    """Инициализация приложения"""
    # Инициализируем БД
    await init_db()
    
    # Создаем приложение
    app = web.Application()
    
    # Добавляем маршруты
    app.router.add_post('/webhook', webhook_handler)
    app.router.add_get('/health', health_check)
    
    return app

async def main():
    """Главная функция"""
    print("🚀 Запускаем локальный сервер...")
    
    # Получаем информацию о боте
    bot_info = await bot.get_me()
    print(f"🤖 Бот: @{bot_info.username}")
    print("📡 Webhook: http://localhost:8080/webhook")
    print("❤️ Health: http://localhost:8080/health")
    print("=" * 50)
    
    app = await init_app()
    
    # Запускаем сервер
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    
    print("✅ Сервер запущен! Нажмите Ctrl+C для остановки")
    
    try:
        # Ждем бесконечно
        await asyncio.Future()
    except KeyboardInterrupt:
        print("\n🛑 Останавливаем сервер...")
    finally:
        await runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
