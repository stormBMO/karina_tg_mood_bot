from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from ..states import ReflectionWizard
from ..db import insert_reflection
from ..practices import get_practices_for_mood, get_encouragement_message
import random

router = Router()

@router.message(F.text == "📝 Новая рефлексия")
async def start_wizard(msg: Message, state: FSMContext):
    await state.set_state(ReflectionWizard.mood)
    await msg.answer("Оцени настроение по шкале 1–5 (1 — плохо, 5 — отлично):")

@router.message(ReflectionWizard.mood, F.text)
async def set_mood(msg: Message, state: FSMContext):
    try:
        mood = int(msg.text)
        if not 1 <= mood <= 5:
            raise ValueError
    except ValueError:
        return await msg.answer("Введи целое число 1..5.")
    await state.update_data(mood=mood)
    await state.set_state(ReflectionWizard.text)
    await msg.answer("Опиши, что повлияло на настроение (1–3 предложения):")

@router.message(ReflectionWizard.text, F.text)
async def set_text(msg: Message, state: FSMContext):
    t = msg.text.strip()
    if len(t) < 10:
        return await msg.answer("Чуть подробнее, пожалуйста (мин. 10 символов).")
    await state.update_data(text=t)
    await state.set_state(ReflectionWizard.tags)
    await msg.answer("Добавь теги через запятую (например: учеба, здоровье) или напиши «пропустить».")

@router.message(ReflectionWizard.tags, F.text)
async def set_tags(msg: Message, state: FSMContext):
    tags = "" if msg.text.lower() == "пропустить" else msg.text
    data = await state.get_data()
    mood = data["mood"]
    
    await insert_reflection(
        msg.from_user.id,
        mood,
        data["text"],
        tags,
    )
    await state.clear()
    
    # Получаем практики для настроения
    practices = get_practices_for_mood(mood)
    encouragement = get_encouragement_message(mood)
    
    if practices:
        # Выбираем случайную практику
        practice = random.choice(practices)
        
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(
            text="🧘 Попробовать практику", 
            callback_data=f"practice_mood_{mood}"
        ))
        builder.row(InlineKeyboardButton(
            text="📊 Посмотреть статистику", 
            callback_data="show_stats"
        ))
        
        text = f"✅ **Записал!**\n\n{encouragement}\n\n"
        text += f"💡 **Рекомендую попробовать:**\n"
        text += f"**{practice.title}**\n"
        text += f"*{practice.description}*\n"
        text += f"⏱️ *Время: {practice.duration}*"
        
        await msg.answer(
            text,
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )
    else:
        await msg.answer(
            f"✅ **Записал!**\n\n{encouragement}\n\n"
            "Возвращайся завтра или посмотри статистику — «📊 Мои показатели».",
            parse_mode="Markdown"
        )

@router.callback_query(F.data == "show_stats")
async def show_stats_from_reflection(callback: CallbackQuery):
    """Показать статистику из рефлексии"""
    from ..db import stats_by_user
    from ..keyboards import main_menu
    
    s = await stats_by_user(callback.from_user.id)
    avg = f"{s['avg_mood']:.2f}" if s["avg_mood"] is not None else "—"
    
    await callback.message.edit_text(
        f"📊 **Ваша статистика**\n\n"
        f"Всего записей: {s['cnt']}\n"
        f"Среднее настроение: {avg}\n\n"
        "Используйте кнопки меню для навигации:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
    await callback.answer()
