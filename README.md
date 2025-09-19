# Учебный Telegram-бот на Python (aiogram v3)

Стартовый проект под идею «Платформа для рефлексии и самопомощи», заточен под защиту: демонстрация **класс/объект, состояние, поведение, индивидуальность** + диаграммы Use‑Case/Activity/Class/Component.

## Структура проекта

```
.
├─ .env.example
├─ requirements.txt
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ config.py
│  ├─ keyboards.py
│  ├─ states.py
│  ├─ db.py
│  ├─ models.py
│  └─ handlers/
│     ├─ __init__.py
│     ├─ common.py
│     └─ reflection.py
└─ data/ (создастся автоматически)
```

## Установка и запуск

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и вставьте ваш BOT_TOKEN
```

4. Запустите бота:
```bash
python -m app.main
```

## Функциональность

- **Рефлексия**: пользователь может оставлять записи с оценкой настроения (1-5) и описанием
- **Статистика**: просмотр количества записей и среднего настроения
- **Экспорт**: выгрузка всех записей в CSV формате
- **Теги**: возможность добавлять теги к записям

## Команды бота

- `/start` — начать работу с ботом
- `/help` — помощь
- `/about` — о проекте

## Мини-модель предмета (для объяснения ООП)

- **Классы**: `User`, `Reflection`, `JournalService` (поведение: добавить/список/статистика), `ExportService`
- **Состояние**: `Reflection.mood 1..5`, `Reflection.tags: str`, `JournalService.db_path`
- **Поведение**: методы сервисов (создать запись, посчитать среднее, выгрузить CSV)
- **Индивидуальность**: уникальный `User.id`

## Что показать на защите

1. Use‑Case: «Пользователь оставляет рефлексию и смотрит статистику»
2. Activity: шаги мастера (настроение → текст → теги → запись)
3. Class: `User`, `Reflection`, `JournalService`, `ExportService`
4. Component: Telegram Bot ↔ DB (SQLite)
5. Демо: /start → «📝 Новая рефлексия» → «📊 Мои показатели» → «📦 Экспорт записей»
