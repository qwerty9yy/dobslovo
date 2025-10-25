from functools import lru_cache
from aiogram.utils.keyboard import InlineKeyboardBuilder

@lru_cache
def get_admin_start_menu():
    ''' Клавиатура меню "Админ стартовое меню" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Статистика', callback_data='statistics')
    builder.button(text='Рассылка', callback_data='mailing')
    builder.button(text='Товары', callback_data='admin_products')
    builder.button(text='Газеты', callback_data='edit_newspapers_photo')
    builder.adjust(1, 1, 2)
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

@lru_cache
def get_admin_products():
    ''' Клавиатура меню "Календари Admin" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить', callback_data='add_calendars')
    builder.button(text='Изменить', callback_data='replace_products')
    builder.button(text='❌ Отменить', callback_data='back_to_admin')
    builder.adjust(2, 1)
    return builder.as_markup()

@lru_cache
def get_add_calendars():
    ''' Клавиатура меню "Календари Добавить или Изменить Admin" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='❌ Отменить', callback_data='cancel_calendars')
    builder.adjust(1)
    return builder.as_markup()
    
@lru_cache
def get_yes_no_change_calendars():
    ''' Клавиатура меню "Подтверждение на удаление и добавлени изображений" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Приступить', callback_data='get_started_change_calendars')
    builder.button(text='❌ Отменить', callback_data='cancel_calendars')
    builder.adjust(1)
    return builder.as_markup()

@lru_cache
def get_edit_newspapers_photo():
    ''' Клавиатура меню "Газета Admin" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить', callback_data='add_newspapers_photo')
    builder.button(text='Изменить', callback_data='replace_newspapers_photo')
    builder.button(text='❌ Отменить', callback_data='back_to_admin')
    builder.adjust(2, 1)
    return builder.as_markup()

@lru_cache
def get_yes_no_replace_newspapers_photo():
    ''' Клавиатура меню "Подтверждение на удаление и добавлени изображений" Telegram-бота «Доброе Слово». '''
    builder = InlineKeyboardBuilder()
    builder.button(text='Приступить', callback_data='started_replace_newspapers_photo')
    builder.button(text='❌ Отменить', callback_data='cancel_calendars')
    builder.adjust(1)
    return builder.as_markup()
