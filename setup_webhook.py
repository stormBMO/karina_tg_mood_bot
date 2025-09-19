#!/usr/bin/env python3
"""
Скрипт для настройки webhook в Telegram Bot API
Используйте после деплоя на Vercel
"""

import asyncio
import os
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

async def setup_webhook():
    """Настройка webhook для бота"""
    
    # Получаем токен бота
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        return
    
    # Получаем URL Vercel (замените на ваш домен)
    vercel_url = input("Введите URL вашего Vercel приложения (например: https://your-app.vercel.app): ")
    if not vercel_url:
        print("❌ URL не указан")
        return
    
    webhook_url = f"{vercel_url}/webhook"
    
    # Создаем бота
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    try:
        # Удаляем старый webhook
        print("🔄 Удаляем старый webhook...")
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Устанавливаем новый webhook
        print(f"🔄 Устанавливаем webhook: {webhook_url}")
        await bot.set_webhook(url=webhook_url)
        
        # Проверяем webhook
        webhook_info = await bot.get_webhook_info()
        print(f"✅ Webhook установлен: {webhook_info.url}")
        print(f"📊 Ожидающих обновлений: {webhook_info.pending_update_count}")
        
    except Exception as e:
        print(f"❌ Ошибка при настройке webhook: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(setup_webhook())
