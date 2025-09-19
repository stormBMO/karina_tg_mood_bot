#!/usr/bin/env python3
"""
Тест локального бота
"""

import asyncio
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
from aiogram.types import Update, Message, User, Chat

# Инициализация бота
bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Регистрация обработчиков
dp.include_router(reflection_handlers.router)
dp.include_router(practices_handlers.router)
dp.include_router(common_handlers.router)

async def test_bot():
    """Тест бота"""
    print("🤖 Тестирование бота для рефлексии и самопомощи")
    print("=" * 60)
    
    # Инициализируем БД
    await init_db()
    
    # Получаем информацию о боте
    bot_info = await bot.get_me()
    print(f"✅ Бот: @{bot_info.username} (ID: {bot_info.id})")
    print(f"📝 Имя: {bot_info.first_name}")
    print()
    
    # Тестируем основные функции
    print("🧪 Тестируем основные функции...")
    
    # Тест 1: Команда /start
    print("1️⃣ Тест команды /start")
    try:
        update = Update(
            update_id=1,
            message=Message(
                message_id=1,
                from_user=User(id=123456789, is_bot=False, first_name="Test"),
                chat=Chat(id=123456789, type="private"),
                date=1640995200,
                text="/start"
            )
        )
        await dp.feed_update(bot, update)
        print("   ✅ /start работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 2: Главное меню
    print("2️⃣ Тест главного меню")
    try:
        update = Update(
            update_id=2,
            message=Message(
                message_id=2,
                from_user=User(id=123456789, is_bot=False, first_name="Test"),
                chat=Chat(id=123456789, type="private"),
                date=1640995200,
                text="📝 Новая рефлексия"
            )
        )
        await dp.feed_update(bot, update)
        print("   ✅ Главное меню работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 3: Практики
    print("3️⃣ Тест системы практик")
    try:
        update = Update(
            update_id=3,
            message=Message(
                message_id=3,
                from_user=User(id=123456789, is_bot=False, first_name="Test"),
                chat=Chat(id=123456789, type="private"),
                date=1640995200,
                text="🧘 Практики"
            )
        )
        await dp.feed_update(bot, update)
        print("   ✅ Система практик работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    
    # Тест 4: Статистика
    print("4️⃣ Тест статистики")
    try:
        update = Update(
            update_id=4,
            message=Message(
                message_id=4,
                from_user=User(id=123456789, is_bot=False, first_name="Test"),
                chat=Chat(id=123456789, type="private"),
                date=1640995200,
                text="📊 Мои показатели"
            )
        )
        await dp.feed_update(bot, update)
        print("   ✅ Статистика работает")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    print()
    print("🎉 Тестирование завершено!")
    print()
    print("💡 Для полного тестирования:")
    print("   1. Запустите: python3 local_server.py")
    print("   2. Установите ngrok: ngrok http 8080")
    print("   3. Настройте webhook: python3 setup_ngrok.py")
    print("   4. Отправьте /start боту в Telegram")

if __name__ == "__main__":
    asyncio.run(test_bot())
