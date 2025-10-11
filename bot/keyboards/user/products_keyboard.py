from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

_cache_data = {'markup': None, 'timestamp': None}
_price_cache = {'markup': None, 'timestamp': None}
_questions_cache = {'markup': None, 'timestamp': None}

support = 'https://t.me/qwert9yy'

def get_products_menu(ozon_link: str):
    """ Клавиатура для меню 'Продукция' """
    now = datetime.now()
    # Обновляем каждые 6 часов
    if not _cache_data['markup'] or (now - _cache_data["timestamp"] > timedelta(hours=12)):
        builder = InlineKeyboardBuilder()
        builder.button(text='🛒 Перейти на Ozon', url=ozon_link)
        builder.button(text='💰 Цена газеты', callback_data='show_price')
        builder.button(text='❓ Популярные вопросы', callback_data='show_faq')
        builder.button(text='🔙 Главное меню', callback_data='back_to_main')
        builder.adjust(1)
        _cache_data['markup'] = builder.as_markup()
        _cache_data['timestamp'] = now
    return _cache_data['markup']

def get_show_price():
    """ Клавиатура для меню 'Цена газеты' """
    now = datetime.now()
    if not _price_cache['markup'] or (now - _price_cache['timestamp'] > timedelta(hours=12)):
        builder = InlineKeyboardBuilder()
        builder.button(text='← Назад', callback_data='menu_products')
        builder.button(text='🔙 Главное меню', callback_data='back_to_main')
        builder.adjust(2)
        _price_cache['markup'] = builder.as_markup()
        _price_cache['timestamp'] = now
    return _price_cache['markup']

def get_show_faq():
    """ Клавиатура для меню 'Популярные вопросы' """
    now = datetime.now()
    if not _questions_cache['markup'] or (now - _questions_cache['timestamp'] > timedelta(hours=12)):
        builder = InlineKeyboardBuilder()
        builder.button(text='🌐 Перейти на сайт', url='https://dobslovo.ru/arhivy-gazety/')
        builder.button(text='💬 Задать вопрос редакции', url=support)
        builder.button(text='← Назад', callback_data='menu_products')
        builder.button(text='🔙 Главное меню', callback_data='back_to_main')
        builder.adjust(1, 1, 2)
        _questions_cache['markup'] = builder.as_markup()
        _questions_cache['timestamp'] = now
    return _questions_cache['markup']