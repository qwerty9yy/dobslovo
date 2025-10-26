import asyncio
import html
import json
import random
from bot.utils.logger import logger
from bot.db import crud
from datetime import datetime, timedelta
from bot.keyboards.user.keyboards import get_contacts_menu, get_menu_about_us, get_menu_newspaper, get_menu_newspaper_search, get_support_us
from bot.keyboards.user.products_keyboard import get_products_menu
from bot.keyboards.user.start_keyboard import get_start_menu
from bot.parsers.archives_parser import parse_archives_page
from bot.parsers.number_newspapers import parse_number_newspapers
from bot.parsers.products_parser import parse_products_page
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from bot.utils.states import NewsPapers

# Глобальная переменная
quote_of_the_day = None

# Загрузка цитат
def load_quotes():
    try:
        with open('bot/cache/bible_qoutes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки цитат: {e}")
        return {'bible_quotes': [], 'christian_words': []}

quotes = load_quotes()

def get_random_message():
    """Возвращает случайную цитату из списка."""
    if not quotes['bible_quotes'] and not quotes['christian_words']:
        return "Доброе слово на сегодня"
    return random.choice(quotes['christian_words'] + quotes['bible_quotes'])

def update_quote_of_the_day():
    """Обновляет глобальную цитату дня."""
    global quote_of_the_day
    quote_of_the_day = get_random_message()
    logger.info(f"Цитата дня обновлена: {quote_of_the_day[:60]}...")

async def quote_updater_loop():
    while True:
        await asyncio.sleep(86400)
        update_quote_of_the_day()

# Инициализируем при загрузке модуля
if quote_of_the_day is None:
    update_quote_of_the_day()


async def show_start_menu(message_or_call, edit: bool = False):
    """Стартовое меню"""
    global quote_of_the_day
    if not quote_of_the_day:
        update_quote_of_the_day()
    text = (
        f"📖 <i>Цитата дня:</i>\n<b>{quote_of_the_day}</b>\n\n"
        
        "🌿 <b>О газете:</b>\n"
        "Издание о Божьей любви, вере и живых свидетельствах людей, "
        "чьи судьбы изменил Христос. Каждое слово здесь — семя надежды!\n\n"
        
        "📚 <b>Что внутри:</b>\n"
        "• Истории спасения и исцеления\n"
        "• Статьи о вере и молитве\n" 
        "• Контакты авторов\n\n"
        
        "🛠 <b>Навигация по боту:</b>\n"
        "/start - Главное меню\n"
        "/newspaper - Читать газету\n" 
        "/products - Наша продукция\n"
        "/donate - Поддержать редакцию\n"
        "/bible - Читать Библию\n"
        "/contacts - Контакты\n"
        "/about - О Нас\n\n"
        
        "💝 <i>Бог любит вас и слышит ваши молитвы!</i>"
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
        "🛍️ <b>ПРИОБРЕСТИ ПРОДУКЦИЮ «Доброе Слово»</b>\n\n"
        
        "📦 <b>В продаже имеется:</b>\n"
        "• Газета «Доброе Слово»\n"
        "• Пластиковые карточки\n"
        "• Календари\n" 
        "• Христианские наклейки\n\n"
        
        "📞 <b>Способы заказа:</b>\n"
        "📩 СМС/Viber/WhatsApp:\n"
        "<code>+7-912-756-82-80</code>\n\n"
        "🛒 Через маркетплейс Ozon и Wildberries\n\n"
        "🕊 <i>Да благословит вас Господь!</i>"
    )
    markup = get_products_menu() # get_products_menu(data['ozon_link'])

    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)

async def show_menu_newspaper(message_or_call, edit: bool = False):
    async def send_or_edit_message(text, markup):
        """Вспомогательная функция для отправки/редактирования сообщения"""
        await asyncio.sleep(0.3)
        if edit and hasattr(message_or_call, 'message'):
            await message_or_call.message.edit_text(text, reply_markup=markup)
        else:
            await message_or_call.answer(text, reply_markup=markup)
    try:
        data = await parse_archives_page()
        newspapers = data.get('newspapers', [])  
        markup = get_menu_newspaper_search(newspapers)
        max_year = max(int(item['year']) for item in newspapers)
        min_year = min(int(item['year']) for item in newspapers)
        text = (
            "📅 <b>Выбор года для чтения</b>\n\n"
            f"🗓 <i>Доступные годы: с {min_year} по {max_year}</i>\n\n"
            "✨ <b>Пусть каждая газета и каждое свидетельство</b>\n"
            "станет благословением для вашей души 🌿"
        )
        await send_or_edit_message(text, markup)
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке архивов: {e}")
        markup = get_menu_newspaper()
        text = '📭 Архивы временно недоступны'
        await send_or_edit_message(text, markup)

    

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


    # "✨ <b>Христианская газета «Доброе Слово»</b>✨\n\n"
    #     "Добро пожаловать в газету <b>«Доброе Слово»</b> — издание, рассказывающее о "
    #     "Божьей любви, вере и живых свидетельствах людей, чьи судьбы изменил Христос.\n\n"
    #     "Мы верим, что каждое доброе слово может стать *семенем надежды* 🌱\n"
    #     "На страницах нашей газеты вы найдёте:\n\n"
    #     "💬 истории реальных людей, которых Бог спас, исцелил и благословил;\n"
    #     "📖 статьи о вере, молитве, милосердии и силе Евангелия;\n"
    #     "🤝 контакты авторов, с которыми вы можете связаться лично.\n\n"
    #     "Пусть каждая публикация станет *ответом на ваш вопрос, "
    #     "ободрением в трудный день и напоминанием, что Бог всегда рядом 🙏\n\n"
    #     "<b>Он любит вас, слышит ваши молитвы и хочет дать вам мир, радость и жизнь с избытком</b> 💖\n\n"
    #     f"📖 <b>{quote_of_the_day}</b>" 