from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder

@lru_cache
def get_start_menu():
    ''' Главное меню Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text="📰 Газета", callback_data="newspaper")
    builder.button(text="📦 Продукция", callback_data="menu_products")
    builder.button(text="🌐 Перейти на сайт", url="https://dobslovo.ru")
    builder.adjust(2, 2, 1)
    return builder.as_markup()
