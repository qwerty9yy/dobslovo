from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder

support = 'https://t.me/qwert9yy'

@lru_cache
def get_contacts_menu():
    ''' Клавиатура меню "Контакты" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='💙 ВКонтакте', url='https://vk.com/dobslovo')
    builder.button(text='🧡 Одноклассники', url='https://ok.ru/dobslovo')
    builder.button(text='💬 Telegram', url='https://t.me/dobslovo')
    builder.button(text='💚 WhatsApp', url='https://chat.whatsapp.com/H286SE95wcTAUjeAG8JhMw')
    builder.button(text='💜 Viber', url='https://invite.viber.com/?g=Nn3Sl2xHHUT-_wcum_56Q5YO1VXFKmsA&lang=ru')
    builder.button(text='💬 Есть вопрос?', url=support)
    builder.button(text="🔙 Главное меню", callback_data="back_to_main")
    builder.adjust(2, 2, 1, 1, 1)
    return builder.as_markup()


@lru_cache
def get_menu_about_us():
    ''' Клавиатура меню "О нас" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='💸 Поддержать', callback_data='donate')
    builder.button(text="🔙 Главное меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()


@lru_cache
def get_support_us():
    ''' Клавиатура меню "Поддержать" Telegram-бота «Доброе Слово». '''
    buider = InlineKeyboardBuilder()
    buider.button(text='🏦 Сбербанк', callback_data='show_sberbank')
    buider.button(text='💳 МТС Банк', callback_data='show_mtsbank')
    buider.button(text='📮 Почта России', callback_data='show_mailrussia')
    buider.button(text='← Назад', callback_data='menu_about_us')
    buider.button(text="🔙 Главное меню", callback_data="back_to_main")
    buider.adjust(1, 1, 1, 2)
    return buider.as_markup()

@lru_cache
def get_show_bank():
   ''' Клавиатура меню "Выбора банка" Telegram-бота «Доброе Слово». '''
   builder = InlineKeyboardBuilder()
   builder.button(text='💬 Есть вопрос?', url=support)
   builder.button(text='← Назад', callback_data='donate')
   builder.button(text='🔙 Главное меню', callback_data='back_to_main')
   builder.adjust(1, 2)
   return builder.as_markup()