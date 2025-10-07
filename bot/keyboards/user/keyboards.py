from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder

@lru_cache
def get_contacts_menu():
    ''' Клавиатура меню "Контакты" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='💙 ВКонтакте', url='https://vk.com/dobslovo')
    builder.button(text='🧡 Одноклассники', url='https://ok.ru/dobslovo')
    builder.button(text='💬 Telegram', url='https://t.me/dobslovo')
    builder.button(text='💚 WhatsApp', url='https://chat.whatsapp.com/H286SE95wcTAUjeAG8JhMw')
    builder.button(text='💜 Viber', url='https://invite.viber.com/?g=Nn3Sl2xHHUT-_wcum_56Q5YO1VXFKmsA&lang=ru')
    builder.button(text="🔙 Главное меню", callback_data="back_to_main")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


@lru_cache
def get_menu_about_us():
    ''' Клавиатура меню "О нас" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='💸 Поддержать', callback_data='support_us')
    builder.button(text="🔙 Главное меню", callback_data="back_to_main")
    builder.adjust(1, 1)
    return builder.as_markup()


@lru_cache
def get_support_us():
    ''' Клавиатура меню "Поддержать" Telegram-бота «Доброе Слово». '''
    buider = InlineKeyboardBuilder()
    buider.button(text='Сбербанк', )
    buider.button(text='МТС', )
    buider.button(text='Почта России', )
    buider.button(text="🔙 Главное меню", callback_data="back_to_main")
    buider.adjust(1)
    return buider.as_markup()