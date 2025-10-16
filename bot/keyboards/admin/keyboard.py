from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder

@lru_cache
def get_admin_start_menu():
    ''' Клавиатура меню "Админ стартовое меню" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Статистика', callback_data='statistics')
    builder.button(text='Рассылка', callback_data='mailing')
    builder.adjust(2)
    return builder.as_markup()

@lru_cache
def get_statistics():
    ''' Клавиатура меню "Статистика" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='В админ панель', callback_data='back_to_admin')
    builder.adjust(1)
    return builder.as_markup()

@lru_cache
def get_mailing():
    ''' Клавиатура меню "Рассылка" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='❌ Отменить', callback_data='cancel_newsletter')
    builder.adjust(1)
    return builder.as_markup()

@lru_cache
def get_newsletter_step():
    ''' Клавиатура меню "Предпросмотр" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Начать рассылку', callback_data='start_newsletter')
    builder.button(text='❌ Отменить', callback_data='cancel_newsletter')
    builder.adjust(2)
    return builder.as_markup()
