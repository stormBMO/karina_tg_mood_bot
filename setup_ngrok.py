#!/usr/bin/env python3
"""
Настройка webhook с ngrok
"""

import os
import requests
import json

def setup_ngrok_webhook():
    """Настроить webhook с ngrok"""
    
    # Токен бота
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
        print("💡 Установите: export BOT_TOKEN='your_bot_token'")
        return
    
    # URL ngrok
    ngrok_url = input("Введите URL ngrok (например: https://abc123.ngrok.io): ").strip()
    if not ngrok_url.startswith("https://"):
        print("❌ URL должен начинаться с https://")
        return
    
    webhook_url = f"{ngrok_url}/webhook"
    
    # URL API Telegram
    api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    
    # Данные для отправки
    data = {
        "url": webhook_url
    }
    
    try:
        print(f"🔄 Настраиваем webhook: {webhook_url}")
        
        # Отправляем запрос
        response = requests.post(api_url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook успешно настроен!")
            
            # Проверяем информацию о webhook
            info_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
            info_response = requests.get(info_url)
            info_result = info_response.json()
            
            if info_result.get("ok"):
                webhook_info = info_result.get("result", {})
                print(f"📊 Ожидающих обновлений: {webhook_info.get('pending_update_count', 0)}")
                print(f"🔗 Текущий webhook: {webhook_info.get('url', 'Не установлен')}")
                
                if webhook_info.get('last_error_message'):
                    print(f"⚠️ Последняя ошибка: {webhook_info.get('last_error_message')}")
        else:
            print("❌ Ошибка при настройке webhook:")
            print(result.get("description", "Неизвестная ошибка"))
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    setup_ngrok_webhook()
