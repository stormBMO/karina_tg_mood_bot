import os
import sys
import asyncio
import json
from typing import Dict, Any

# Добавляем путь к приложению
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def handler(request: Dict[str, Any]) -> Dict[str, Any]:
    """Vercel serverless function handler"""
    
    # Получаем HTTP метод
    method = request.get('method', 'GET')
    
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Bot is running!'
        }
    
    elif method == 'POST':
        try:
            # Получаем тело запроса
            body = request.get('body', '{}')
            if isinstance(body, str):
                update_data = json.loads(body)
            else:
                update_data = body
            
            # Обрабатываем обновление
            result = asyncio.run(process_update(update_data))
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'ok': True})
            }
            
        except Exception as e:
            print(f"Error processing update: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'ok': False, 'error': str(e)})
            }
    
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        }

async def process_update(update_data: Dict[str, Any]):
    """Обработка обновления от Telegram"""
    try:
        # Импортируем модули внутри функции для лучшей совместимости
        from app.config import cfg
        from app.db import init_db
        from app.handlers import common as common_handlers
        from app.handlers import reflection as reflection_handlers
        from app.handlers import practices as practices_handlers
        
        from aiogram import Bot, Dispatcher
        from aiogram.client.default import DefaultBotProperties
        from aiogram.enums import ParseMode
        from aiogram.types import Update
        
        # Инициализация бота
        bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()
        
        # Регистрация обработчиков
        dp.include_router(reflection_handlers.router)
        dp.include_router(practices_handlers.router)
        dp.include_router(common_handlers.router)
        
        # Инициализируем БД
        await init_db()
        
        # Создаем объект Update
        update = Update(**update_data)
        
        # Обрабатываем обновление
        await dp.feed_update(bot, update)
        
        # Закрываем сессию бота
        await bot.session.close()
        
    except Exception as e:
        print(f"Error in process_update: {e}")
        raise e
