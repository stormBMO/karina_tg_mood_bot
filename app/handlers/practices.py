from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from ..practices import get_practices_for_mood, get_practices_by_category, get_random_practice, get_encouragement_message
from ..db import stats_by_user
import random

router = Router()

@router.message(F.text == "🧘 Практики")
async def show_practices_menu(msg: Message):
    """Показать меню практик"""
    builder = InlineKeyboardBuilder()
    
    # Получаем последнее настроение пользователя для рекомендации
    stats = await stats_by_user(msg.from_user.id)
    last_mood = 3  # По умолчанию нейтральное
    
    if stats['cnt'] > 0:
        # Здесь можно было бы получить последнее настроение из БД
        # Пока используем случайное для демонстрации
        last_mood = random.randint(1, 5)
    
    builder.row(InlineKeyboardButton(
        text="🎯 Рекомендация по настроению", 
        callback_data=f"practice_mood_{last_mood}"
    ))
    builder.row(
        InlineKeyboardButton(text="🌬️ Дыхание", callback_data="practice_category_дыхание"),
        InlineKeyboardButton(text="🧘‍♀️ Движение", callback_data="practice_category_движение")
    )
    builder.row(
        InlineKeyboardButton(text="📝 Рефлексия", callback_data="practice_category_рефлексия"),
        InlineKeyboardButton(text="🎲 Случайная практика", callback_data="practice_random")
    )
    
    await msg.answer(
        "🧘 **Практики для саморазвития**\n\n"
        "Выберите тип практики или получите персональную рекомендацию на основе вашего настроения:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("practice_mood_"))
async def show_practices_by_mood(callback: CallbackQuery):
    """Показать практики для определенного настроения"""
    mood = int(callback.data.split("_")[-1])
    practices = get_practices_for_mood(mood)
    
    if not practices:
        await callback.answer("Практики для этого настроения не найдены")
        return
    
    # Выбираем случайную практику
    practice = random.choice(practices)
    
    encouragement = get_encouragement_message(mood)
    
    text = f"{encouragement}\n\n"
    text += f"**{practice.title}**\n\n"
    text += f"📝 *{practice.description}*\n"
    text += f"⏱️ *Время: {practice.duration}*\n\n"
    text += "**Шаги:**\n"
    
    for i, step in enumerate(practice.steps, 1):
        text += f"{i}. {step}\n"
    
    text += f"\n💡 *Категория: {practice.category}*"
    
    try:
        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="🔄 Другая практика", callback_data=f"practice_mood_{mood}"),
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_practices")
            ).as_markup()
        )
    except Exception:
        # Если сообщение не изменилось, просто отвечаем на callback
        await callback.answer("Попробуйте еще раз!")
    else:
        await callback.answer()

@router.callback_query(F.data.startswith("practice_category_"))
async def show_practices_by_category(callback: CallbackQuery):
    """Показать практики по категории"""
    category = callback.data.split("_")[-1]
    practices = get_practices_by_category(category)
    
    if not practices:
        await callback.answer("Практики этой категории не найдены")
        return
    
    practice = random.choice(practices)
    
    text = f"**{practice.title}**\n\n"
    text += f"📝 *{practice.description}*\n"
    text += f"⏱️ *Время: {practice.duration}*\n\n"
    text += "**Шаги:**\n"
    
    for i, step in enumerate(practice.steps, 1):
        text += f"{i}. {step}\n"
    
    text += f"\n💡 *Категория: {practice.category}*"
    
    try:
        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="🔄 Другая практика", callback_data=f"practice_category_{category}"),
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_practices")
            ).as_markup()
        )
    except Exception:
        await callback.answer("Попробуйте еще раз!")
    else:
        await callback.answer()

@router.callback_query(F.data == "practice_random")
async def show_random_practice(callback: CallbackQuery):
    """Показать случайную практику"""
    mood = random.randint(1, 5)
    practice = get_random_practice(mood)
    
    if not practice:
        await callback.answer("Практики не найдены")
        return
    
    text = f"🎲 **Случайная практика**\n\n"
    text += f"**{practice.title}**\n\n"
    text += f"📝 *{practice.description}*\n"
    text += f"⏱️ *Время: {practice.duration}*\n\n"
    text += "**Шаги:**\n"
    
    for i, step in enumerate(practice.steps, 1):
        text += f"{i}. {step}\n"
    
    text += f"\n💡 *Категория: {practice.category}*"
    
    try:
        await callback.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardBuilder().row(
                InlineKeyboardButton(text="🎲 Еще одна", callback_data="practice_random"),
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_practices")
            ).as_markup()
        )
    except Exception:
        await callback.answer("Попробуйте еще раз!")
    else:
        await callback.answer()

@router.callback_query(F.data == "back_to_practices")
async def back_to_practices_menu(callback: CallbackQuery):
    """Вернуться к меню практик"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="🎯 Рекомендация по настроению", 
        callback_data="practice_mood_3"
    ))
    builder.row(
        InlineKeyboardButton(text="🌬️ Дыхание", callback_data="practice_category_дыхание"),
        InlineKeyboardButton(text="🧘‍♀️ Движение", callback_data="practice_category_движение")
    )
    builder.row(
        InlineKeyboardButton(text="📝 Рефлексия", callback_data="practice_category_рефлексия"),
        InlineKeyboardButton(text="🎲 Случайная практика", callback_data="practice_random")
    )
    
    await callback.message.edit_text(
        "🧘 **Практики для саморазвития**\n\n"
        "Выберите тип практики или получите персональную рекомендацию на основе вашего настроения:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()
