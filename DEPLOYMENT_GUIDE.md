# 🚀 Деплой Telegram-бота на Vercel

## 📋 Подготовка

### 1. Установите Vercel CLI
```bash
npm install -g vercel
```

### 2. Войдите в аккаунт Vercel
```bash
vercel login
```

## 🔧 Настройка проекта

### 1. Структура файлов
Убедитесь, что у вас есть следующие файлы:
```
karina-tg/
├── api/
│   └── webhook.py          # Обработчик webhook
├── app/                    # Основное приложение
├── vercel.json            # Конфигурация Vercel
├── requirements.txt       # Зависимости Python
└── setup_webhook.py       # Скрипт настройки webhook
```

### 2. Переменные окружения
Создайте файл `.env.local` (не коммитьте в git):
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
DATABASE_PATH=/tmp/db.sqlite
```

## 🚀 Деплой

### 1. Инициализация проекта
```bash
cd karina-tg
vercel
```

Следуйте инструкциям:
- **Set up and deploy?** → `Y`
- **Which scope?** → выберите ваш аккаунт
- **Link to existing project?** → `N`
- **What's your project's name?** → `karina-tg-bot` (или любое другое)
- **In which directory is your code located?** → `./`

### 2. Настройка переменных окружения
```bash
vercel env add BOT_TOKEN
# Введите ваш токен бота

vercel env add ADMIN_IDS
# Введите ID администраторов через запятую

vercel env add DATABASE_PATH
# Введите: /tmp/db.sqlite
```

### 3. Деплой
```bash
vercel --prod
```

## 🔗 Настройка Webhook

### 1. Получите URL вашего приложения
После деплоя Vercel покажет URL вида:
```
https://karina-tg-bot-xxx.vercel.app
```

### 2. Настройте webhook
```bash
# Установите переменную окружения
export BOT_TOKEN="your_bot_token_here"

# Запустите скрипт настройки
python3 setup_webhook.py
```

Введите URL вашего Vercel приложения когда попросит.

### 3. Проверьте webhook
Откройте в браузере:
```
https://your-app.vercel.app/webhook
```

Должно показать: `Bot is running!`

## 🧪 Тестирование

### 1. Проверьте бота в Telegram
- Найдите вашего бота по username
- Отправьте `/start`
- Проверьте все функции

### 2. Проверьте логи
```bash
vercel logs
```

## 🔄 Обновление

### 1. Внесите изменения в код
### 2. Деплойте обновления
```bash
vercel --prod
```

### 3. Webhook обновится автоматически

## 🛠️ Устранение проблем

### Проблема: Бот не отвечает
**Решение:**
1. Проверьте переменные окружения: `vercel env ls`
2. Проверьте логи: `vercel logs`
3. Убедитесь, что webhook настроен правильно

### Проблема: Ошибка 500
**Решение:**
1. Проверьте логи Vercel
2. Убедитесь, что все зависимости установлены
3. Проверьте синтаксис Python кода

### Проблема: База данных не работает
**Решение:**
1. Vercel использует `/tmp/` для временных файлов
2. База данных сбрасывается при каждом деплое
3. Для продакшена рассмотрите внешнюю БД (PostgreSQL, MongoDB)

## 📊 Мониторинг

### 1. Логи Vercel
```bash
vercel logs --follow
```

### 2. Метрики в дашборде Vercel
- Перейдите на vercel.com
- Откройте ваш проект
- Смотрите раздел "Functions" для метрик

## 🔒 Безопасность

### 1. Не коммитьте токены
- Добавьте `.env.local` в `.gitignore`
- Используйте переменные окружения Vercel

### 2. Ограничьте доступ
- Используйте `ADMIN_IDS` для ограничения функций
- Регулярно обновляйте токены

## 💰 Стоимость

### Vercel Free Tier:
- ✅ 100GB bandwidth в месяц
- ✅ 100GB-hours serverless function execution
- ✅ Неограниченное количество деплоев
- ✅ SSL сертификаты

### Для высоконагруженных ботов:
- Рассмотрите Vercel Pro ($20/месяц)
- Или используйте VPS с постоянным процессом

## 🎯 Готово!

Ваш бот теперь доступен 24/7 на Vercel! 

**URL webhook:** `https://your-app.vercel.app/webhook`
**Бот в Telegram:** `@your_bot_username`

---

*Примечание: Vercel отлично подходит для ботов с умеренной нагрузкой. Для высоконагруженных проектов рассмотрите VPS или специализированные платформы для ботов.*
