from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from ..keyboards import main_menu
from ..db import upsert_user, stats_by_user, list_reflections
from io import StringIO
import csv
from datetime import datetime

router = Router()

@router.message(F.text == "/start")
async def cmd_start(msg: Message):
    await upsert_user(msg.from_user)
    await msg.answer(
        "Привет! Я бот для рефлексии и самопомощи. Нажми «📝 Новая рефлексия», чтобы начать.",
        reply_markup=main_menu(),
    )

@router.message(F.text == "/help")
async def cmd_help(msg: Message):
    await msg.answer("/start — начать\n/help — помощь\n/about — о проекте")

@router.message(F.text == "/about")
async def cmd_about(msg: Message):
    await msg.answer("Платформа для рефлексии: короткие заметки, оценка настроения 1–5, статистика и экспорт.")

@router.message(F.text == "📊 Мои показатели")
async def my_stats(msg: Message):
    s = await stats_by_user(msg.from_user.id)
    avg = f"{s['avg_mood']:.2f}" if s["avg_mood"] is not None else "—"
    await msg.answer(
        f"📊 **Ваша статистика**\n\n"
        f"Всего записей: {s['cnt']}\n"
        f"Среднее настроение: {avg}",
        parse_mode="Markdown"
    )

@router.message(F.text == "📦 Экспорт записей")
async def export_csv(msg: Message):
    rows = await list_reflections(msg.from_user.id)
    sio = StringIO()
    w = csv.DictWriter(sio, fieldnames=["created_at", "mood", "text", "tags"]) 
    w.writeheader()
    for r in rows:
        iso = datetime.fromtimestamp(r["created_at"]/1000).isoformat()
        w.writerow({"created_at": iso, **{k: r[k] for k in ("mood","text","tags")}})
    data = sio.getvalue().encode("utf-8")
    document = BufferedInputFile(data, filename="reflections.csv")
    await msg.answer_document(document=document)

@router.message()
async def unknown_message(msg: Message):
    await msg.answer("Не понимаю эту команду. Используй кнопки меню или команды /start, /help", reply_markup=main_menu())
