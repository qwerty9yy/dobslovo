import html
from bot.db import crud
from bot.keyboards.user.keyboards import get_contacts_menu, get_menu_about_us, get_menu_newspaper, get_support_us
from bot.keyboards.user.products_keyboard import get_products_menu
from bot.keyboards.user.start_keyboard import get_start_menu
from bot.parsers.number_newspapers import parse_number_newspapers
from bot.parsers.products_parser import parse_products_page
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from bot.utils.states import NewsPapers

async def show_start_menu(message_or_call, edit: bool = False):
    """Стартовое меню"""
    text = (
        "✨ <b>Христианская газета «Доброе Слово»</b>✨\n\n"
        "<i>«Ибо так возлюбил Бог мир, что отдал Сына Своего Единородного, "
        "дабы всякий верующий в Него не погиб, но имел жизнь вечную»\n"
        "📖 Иоанна 3:16</i>\n\n"
        "Добро пожаловать в газету <b>«Доброе Слово»</b> — издание, рассказывающее о "
        "Божьей любви, вере и живых свидетельствах людей, чьи судьбы изменил Христос.\n\n"
        "Мы верим, что каждое доброе слово может стать *семенем надежды* 🌱\n"
        "На страницах нашей газеты вы найдёте:\n\n"
        "💬 истории реальных людей, которых Бог спас, исцелил и благословил;\n"
        "📖 статьи о вере, молитве, милосердии и силе Евангелия;\n"
        "🎥 видео-свидетельства о Божьих чудесах в современном мире;\n"
        "🤝 контакты авторов, с которыми вы можете связаться лично.\n\n"
        "Пусть каждая публикация станет *ответом на ваш вопрос, "
        "ободрением в трудный день и напоминанием, что Бог всегда рядом 🙏\n\n"
        "<b>Он любит вас, слышит ваши молитвы и хочет дать вам *мир, радость и жизнь с избытком*</b> 💖\n\n"
    )
    markup = get_start_menu()
    if edit and hasattr(message_or_call, "message"):
        try:
            await message_or_call.message.edit_text(text, reply_markup=markup)
        except TelegramBadRequest:
            await message_or_call.message.answer(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)
        
        
async def show_menu_contacts(message_or_call, edit: bool = False):
    """Меню Контакты"""
    text =(
        "🌿 <b>Христианская газета «Доброе Слово»</b>\n\n"
        "Присоединяйтесь к нашим сообществам, где ежедневно публикуются "
        "ободряющие и вдохновляющие христианские материалы. 🙏\n\n"
        "📞 Телефон: +7-912-756-82-80\n\n"
        "<i>Пусть каждое слово приносит свет и надежду в ваш день.</i> ✨"
    )
    markup = get_contacts_menu()
    if edit and hasattr(message_or_call, "message"):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)
        
        
async def show_menu_about_us(message_or_call, edit: bool = False):
    """Меню О нас"""
    data = await parse_number_newspapers()
    newspapers = data.get('count_newspapers')
    text = (
        "✨ <b>О нас</b> ✨\n\n"
        "История христианской газеты <b>«Доброе Слово»</b> началась ещё в <b>2002 году</b>. "
        "С первых выпусков мы стремились рассказывать о Божьей любви и о том, "
        "как Господь действует в жизни обычных людей.\n\n"
        f"Газет отпечатано с 2002 года: <b>{newspapers}</b>\n\n"
        "🕊️ На страницах нашей газеты вы найдёте:\n"
        "• вдохновляющие свидетельства о вере и чудесах Божьих,\n"
        "• поучительные статьи и размышления,\n"
        "• добрые истории, которые укрепляют дух,\n"
        "• стихи и слова утешения из Писания.\n\n"
        "Наша цель — чтобы через каждую статью звучало <b>Слово Жизни</b>, "
        "которое способно коснуться сердца и изменить судьбу человека.\n\n"
        "📖 Как сказано в Библии:\n"
        "<i>«Ибо слово Божие живо и действенно и острее всякого меча обоюдоострого...»</i>\n"
        "(Послание к Евреям 4:12)\n\n"
        "🙏 Пусть каждое доброе слово станет для вас благословением, "
        "а газета — источником надежды и радости!"
    )
    markup = get_menu_about_us()
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)

async def show_donate_menu(message_or_call, edit: bool = False):
    """Меню Поддержать"""
    text = (
        "💖 <b>Поддержать газету «Доброе Слово»</b>\n\n"
        "Спасибо всем, кто распространяет газету и поддерживает редакцию финансово!\n"
        "Благодаря вашим пожертвованиям мы можем продолжать выпускать и рассылать газету.\n\n"
        "Просим вас по возможности участвовать в служении и далее — "
        "а также рассказать о газете другим верующим, чтобы и они могли благовествовать через неё.\n\n"
        "🙏 <b>Да благословит вас Господь!</b>"
    )
    markup = get_support_us()
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)
        
async def show_products_menu(message_or_call, edit: bool = False):
    """Меню продукция"""
    data = await parse_products_page()
    text = (
        "📰 <b>Заказать и купить газету «Доброе Слово»</b> можно:\n\n"
        "📩 Отправив сообщение по СМС, Viber или WhatsApp на номер:\n"
        "<code>+7-912-756-82-80</code>\n\n"
        "🛍️ Или через маркетплейс Ozon:"
    )
    markup = get_products_menu(data['ozon_link'])
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)

async def show_menu_newspaper(message_or_call, edit: bool = False):
    text = (
        "📅 Напишите, за какой год вы хотите посмотреть газеты.\n\n"
        "Например: <b>2024</b>"
    )
    markup = get_menu_newspaper()
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)
    
    
        

# async def show_newspaper_menu(message_or_call, edit: bool = False):
#     """Меню Газета"""
#     text = (
#         "📅 Напишите, за какой год вы хотите посмотреть газеты.\n\n"
#         "Например: <b>2024</b>"
#     )
#     if edit and hasattr(message_or_call, 'message'):
#         await message_or_call.message.edit_text(text)
#     else:
#         await message_or_call.answer(text)

# async def show_resources_menu(message_or_call, edit: bool = False):
#     """Меню"""
#     # Текст меню (одинаковый для команды и кнопки)
#     text = ""
#     # Получаем клавиатуру из существующего файла
#     markup = get_resources_menu()

#     # Решаем, редактировать сообщение или отправить новое
#     if edit and hasattr(message_or_call, "message"):
#         # Для CallbackQuery: редактируем текущее сообщение
#         await message_or_call.message.edit_text(text, reply_markup=markup)
#     else:
#         # Для Message: отправляем новое сообщение
#         await message_or_call.answer(text, reply_markup=markup)