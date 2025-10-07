import html
from bot.db import crud
from bot.keyboards.user.keyboards import get_contacts_menu, get_menu_about_us
from bot.keyboards.user.start_keyboard import get_start_menu

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
        await message_or_call.message.edit_text(text, reply_markup=markup)
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
    text = ('О нас\n')
    markup = get_menu_about_us()
    if edit and hasattr(message_or_call, 'message'):
        await message_or_call.message.edit_text(text, reply_markup=markup)
    else:
        await message_or_call.answer(text, reply_markup=markup)

    

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