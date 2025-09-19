# 🚀 Быстрый старт: Деплой на Vercel

## ⚡ За 5 минут

### 1. Установите Vercel CLI
```bash
npm install -g vercel
```

### 2. Войдите в Vercel
```bash
vercel login
```

### 3. Деплойте проект
```bash
cd karina-tg
vercel
```

### 4. Настройте переменные окружения
```bash
vercel env add BOT_TOKEN
# Введите токен вашего бота

vercel env add ADMIN_IDS  
# Введите ID администраторов через запятую

vercel env add DATABASE_PATH
# Введите: /tmp/db.sqlite
```

### 5. Настройте webhook
```bash
# Установите токен
export BOT_TOKEN="your_bot_token_here"

# Настройте webhook
python3 setup_webhook.py
# Введите URL вашего Vercel приложения
```

## ✅ Готово!

Ваш бот работает на Vercel! 🎉

**URL:** `https://your-app.vercel.app/webhook`

---

*Подробная инструкция в `DEPLOYMENT_GUIDE.md`*
