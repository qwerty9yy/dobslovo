from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

# _cache_data = {'markup': None, 'timestamp': None}
# _price_cache = {'markup': None, 'timestamp': None}
# _questions_cache = {'markup': None, 'timestamp': None}

support = 'https://t.me/sergey_kocsheev'
URL = 'https://dobslovo.ru/'
wildberries= 'https://www.wildberries.ru/seller/4271588'
ozon = 'https://www.ozon.ru/seller/dobroe-slovo-1431319/products/?miniapp=seller_1431319&sorting=new&__rr=1'
@lru_cache
def get_products_menu():
    """ Клавиатура для меню 'Продукция' """
    # now = datetime.now()
    # # Обновляем каждые 12 часов
    # if not _cache_data['markup'] or (now - _cache_data["timestamp"] > timedelta(hours=12)):
    builder = InlineKeyboardBuilder()
    builder.button(text='🛒 Ozon', url=ozon)
    builder.button(text='🛒 Wildberries', url=wildberries)
    builder.button(text='🛍️ Товары', callback_data='products_dobslovo')
    # builder.button(text='💰 Цена газеты', callback_data='show_price')
    builder.button(text='❓ Популярные вопросы', callback_data='show_faq')
    builder.button(text="🌐 Перейти на сайт", url=f"{URL}/kupit-gazetu/")
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2, 1)
        # _cache_data['markup'] = builder.as_markup()
        # _cache_data['timestamp'] = now
    # return _cache_data['markup']
    return builder.as_markup()

@lru_cache
def get_failed_products_dobslovo():
    builder = InlineKeyboardBuilder()
    builder.button(text='← Назад', callback_data='menu_products')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2)
    return builder.as_markup()

@lru_cache
def get_failed_newspaper_products_dobslovo():
    builder = InlineKeyboardBuilder()
    builder.button(text='← Назад', callback_data='products_dobslovo')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2)
    return builder.as_markup()

@lru_cache
def get_products_dobslovo():
    builder = InlineKeyboardBuilder()
    builder.button(text='📖 Газета', callback_data='products_dobslovo_newspaper_photo')
    builder.button(text='🛒 Ozon', url=ozon)
    builder.button(text='🛒 Wildberries', url=wildberries)
    builder.button(text='← Назад', callback_data='menu_products')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(1, 2)
    return builder.as_markup()

@lru_cache
def get_newspaper_products_dobslovo():
    builder = InlineKeyboardBuilder()
    builder.button(text='🛒 Ozon', url=ozon)
    builder.button(text='🛒 Wildberries', url=wildberries)
    builder.button(text='← Назад', callback_data='menu_products')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2, 2)
    return builder.as_markup()

@lru_cache
def get_show_price():
    """ Клавиатура для меню 'Цена газеты' """
    builder = InlineKeyboardBuilder()
    builder.button(text='← Назад', callback_data='menu_products')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(2)
    return builder.as_markup()

@lru_cache
def get_show_faq():
    """ Клавиатура для меню 'Популярные вопросы' """
    # now = datetime.now()
    # if not _questions_cache['markup'] or (now - _questions_cache['timestamp'] > timedelta(hours=12)):
    builder = InlineKeyboardBuilder()
    builder.button(text='🌐 Перейти на сайт', url='https://dobslovo.ru/arhivy-gazety/')
    builder.button(text='💬 Задать вопрос редакции', url=support)
    builder.button(text='← Назад', callback_data='menu_products')
    builder.button(text='🔙 Главное меню', callback_data='back_to_main')
    builder.adjust(1, 1, 2)
        # _questions_cache['markup'] = builder.as_markup()
        # _questions_cache['timestamp'] = now
    # return _questions_cache['markup']
    return builder.as_markup()