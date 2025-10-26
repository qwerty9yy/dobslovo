"""Объяснение:

Простейшая проверка прав администратора по ADMIN_ID.

Если ID не совпадает — отправляем отказ.

Легко расширяется до полноценной админ-панели."""

import asyncio
import os
import datetime
from bot.filters.admin import IsAdmin
from aiogram import Bot, Router, types, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.utils.logger import logger
from bot.db.appeal_bd import get_all_users_tg_id, get_user_count
from bot.keyboards.admin.keyboard import get_add_calendars, get_admin_products, get_admin_start_menu, get_edit_newspapers_photo, get_mailing, get_newsletter_step, get_statistics, get_yes_no_change_calendars, get_yes_no_replace_newspapers_photo
from bot.utils.states import AdminState

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())

MEDIA_PRODUCTS_DIR = "bot/media/products"
MEDIA_NEWSPAPER_DIR = "bot/media/newspaper"

@admin_router.message(Command("admin"))
async def admin_panel(message: types.Message):
    await message.answer("✅ Добро пожаловать в админку!", 
                         reply_markup=get_admin_start_menu())

@admin_router.callback_query(F.data == 'back_to_admin')
async def back_to_admin_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "✅ Добро пожаловать в админку!", 
        reply_markup=get_admin_start_menu()
    )
    
@admin_router.callback_query(F.data == 'statistics')
async def admin_menu_statistics(callback: CallbackQuery):
    """Меню Статистика"""
    count = await get_user_count()
    text = (
        '📊 Статистика\n\n'
        f'👥 Пользователей: {count}'
    )
    markup = get_statistics()
    await callback.message.edit_text(text, reply_markup=markup)

@admin_router.callback_query(F.data == 'mailing')
async def admin_menu_mailing(callback: CallbackQuery, state: FSMContext):
    """Меню Рассылка"""
    text = (
        '📨 Рассылка\n\n'
        'Введите сообщение для отправки всем пользователям:'
    )
    markup = get_mailing()
    await callback.message.edit_text(text, reply_markup=markup)
    await state.set_state(AdminState.newsletter)

@admin_router.callback_query(F.data == 'cancel_newsletter')
async def admin_cancel_newsletter(callback: CallbackQuery, state: FSMContext):
    """Меню Отмена Рассылка"""
    await state.clear()
    text = '❌ Рассылка отменена'
    await callback.answer(text, show_alert=False)
    await back_to_admin_callback(callback)

@admin_router.message(AdminState.newsletter)
async def admin_newsletter_step(message: types.Message, state:FSMContext, bot: Bot):
    """Получаем сообщение для рассылки и показываем превью"""
    preview_text = (
        "📨 Предпросмотр рассылки:\n\n"
        "Сообщение будет отправлено всем пользователям."        
    )
    # Отправляем копию сообщения + кнопки
    await message.send_copy(message.chat.id)
    preview_msg = await message.answer(preview_text, reply_markup=get_newsletter_step())
    
    await state.update_data(
        newsletter_message_id=message.message_id,
        newsletter_chat_id=message.chat.id,
        preview_message_id=preview_msg.message_id  # Сохраняем ID превью для удаления
    )
    
@admin_router.callback_query(F.data == 'start_newsletter')
async def start_newsletter_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Запуск рассылки с прогресс-баром"""
    user_data = await state.get_data()
    all_ids = await get_all_users_tg_id()
    total_users = len(all_ids)
    success = 0
    failed = 0
    
    # Удаляем сообщение с превью
    try:
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=user_data['preview_message_id']
        )
    except:
        pass
    
    # Сообщение о начале рассылки
    progress_msg = await callback.message.answer(
        f'🔄 Начата рассылка для {total_users} пользователей...\n'
        f"0/{total_users} отправлено"        
    )
    
    # Отправка сообщений с обновлением прогресса
    for i, user_id in enumerate(all_ids, 1):
        try:
            await bot.copy_message(
                chat_id=user_id,
                from_chat_id=user_data['newsletter_chat_id'],
                message_id=user_data['newsletter_message_id']                
            )
            success += 1
            
            # Обновляем прогресс каждые 10 отправок
            if i % 10 == 0 or i == total_users:
                await progress_msg.edit_text(
                    f'🔄 Рассылка...\n'
                    f"{i}/{total_users} отправлено\n"
                    f"✅ Успешно: {success}\n"
                    f"❌ Ошибок: {failed}"                    
                )
            await asyncio.sleep(0.3)
        except Exception as e:
            failed += 1
            logger.error(f"Ошибка отправки пользователю {user_id}: {e}")            
            
    # Итоговое сообщение
    result_message = (
        f"✅ Рассылка завершена!\n\n"
        f"👥 Всего пользователей: {total_users}\n"
        f"✅ Успешно отправлено: {success}\n"
        f"❌ Не удалось отправить: {failed}"
    )
    await progress_msg.edit_text(result_message, reply_markup=get_statistics())
    await state.clear()

@admin_router.callback_query(F.data == 'cancel_calendars')
async def admin_cancel_calendars(callback: CallbackQuery, state: FSMContext):
    """Меню Отмена Замены изображения"""
    await state.clear()
    await back_to_admin_callback(callback)

@admin_router.callback_query(F.data == 'admin_products')
async def admin_calendars(callback: CallbackQuery):
    """Меню Замена изображения в рекламе Календари"""
    text = (
        "🖼 **Управление Изображениями товаров в продукции**\n\n"
        "✨ Здесь вы можете управлять изображениями товаров для рекламы:\n\n"
        "• **Добавить** - добавить новое изображение к существующим\n"
        "• **Изменить** - удалить старые изображения и заменить на новые\n\n"
        "👇 Выберите действие:"        
    )
    markup = get_admin_products()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')
    
@admin_router.callback_query(F.data == 'add_calendars')
async def admin_add_calendars(callback: CallbackQuery, state: FSMContext):
    """Меню Добавления изображения в рекламе Календари"""
    os.makedirs(MEDIA_PRODUCTS_DIR, exist_ok=True)
    text = (
        '📸 Отправьте одно или несколько изображений:'
    )
    await state.set_state(AdminState.add_and_change_calendars)
    markup = get_add_calendars()
    await callback.message.edit_text(text, reply_markup=markup)

@admin_router.message(AdminState.add_and_change_calendars, F.photo)
async def handle_add_products(message: types.Message, state: FSMContext):
    os.makedirs(MEDIA_PRODUCTS_DIR, exist_ok=True)
    for photo in message.photo[-1:]:
        
        file = await message.bot.get_file(photo.file_id)
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{photo.file_id}.jpg"
        file_path = os.path.join(MEDIA_PRODUCTS_DIR, filename)
        await message.bot.download_file(file.file_path, file_path)
        
    markup = get_statistics()
    await message.answer('✅ Изрбражение успешно добавлено!', reply_markup=markup)
    await state.clear()

# Изменение (удаляем и добавляем заново)
@admin_router.callback_query(F.data == 'replace_products')
async def admin_replace_products(callback: CallbackQuery):
    text = (
        "⚠️ **Подтверждение удаления**\n\n"
        "❗️ *Вы уверены в этом действии?*\n\n"
        "🗑️ Все изображения в этом разделе будут **безвозвратно удалены**"
    )
    markup = get_yes_no_change_calendars()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')

@admin_router.callback_query(F.data == 'get_started_change_calendars')
async def get_started_change_calendars(callback: types.CallbackQuery, state: FSMContext):
    os.makedirs(MEDIA_PRODUCTS_DIR, exist_ok=True)
    
    listdir = os.listdir(MEDIA_PRODUCTS_DIR)
    for file in listdir:
        os.remove(os.path.join(MEDIA_PRODUCTS_DIR, file))
    
    await state.set_state(AdminState.add_and_change_calendars)
    markup = get_add_calendars()
    await callback.message.edit_text('♻️ Все старые изображения удалены.\nТеперь отправьте новые изображения.',
                                     reply_markup=markup)

@admin_router.callback_query(F.data == 'edit_newspapers_photo')
async def edit_newspapers_photo(callback: CallbackQuery):
    """Меню Замена изображения в рекламе Газета"""
    text = (
        "🖼 **Управление Изображениями газеты в продукции**\n\n"
        "✨ Здесь вы можете управлять изображениями газеты для рекламы:\n\n"
        "• **Добавить** - добавить новое изображение к существующим\n"
        "• **Изменить** - удалить старые изображения и заменить на новые\n\n"
        "👇 Выберите действие:"   
    )
    markup = get_edit_newspapers_photo()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')

@admin_router.callback_query(F.data == 'add_newspapers_photo')
async def admin_add_newspapers_photo(callback: CallbackQuery, state: FSMContext):
    """Меню Добавления изображения в рекламе Гаезта"""
    os.makedirs(MEDIA_NEWSPAPER_DIR, exist_ok=True)
    text = (
        '📸 Отправьте одно или несколько изображений:'
    )
    await state.set_state(AdminState.edit_newspapers_photo)
    markup = get_add_calendars()
    await callback.message.edit_text(text, reply_markup=markup)

# Изменение (удаляем и добавляем заново)
@admin_router.callback_query(F.data == 'replace_newspapers_photo')
async def admin_replace_newspapers_photo(callback: CallbackQuery):
    text = (
        "⚠️ **Подтверждение удаления**\n\n"
        "❗️ *Вы уверены в этом действии?*\n\n"
        "🗑️ Все изображения в этом разделе будут **безвозвратно удалены**"
    )
    markup = get_yes_no_replace_newspapers_photo()
    await callback.message.edit_text(text, reply_markup=markup, parse_mode='Markdown')

@admin_router.callback_query(F.data == 'started_replace_newspapers_photo')
async def get_started_replace_newspapers_photo(callback: types.CallbackQuery, state: FSMContext):
    os.makedirs(MEDIA_NEWSPAPER_DIR, exist_ok=True)
    
    listdir = os.listdir(MEDIA_NEWSPAPER_DIR)
    for file in listdir:
        os.remove(os.path.join(MEDIA_NEWSPAPER_DIR, file))
    
    await state.set_state(AdminState.edit_newspapers_photo)
    markup = get_add_calendars()
    await callback.message.edit_text('♻️ Все старые изображения удалены.\nТеперь отправьте новые изображения.',
                                     reply_markup=markup)

@admin_router.message(AdminState.edit_newspapers_photo, F.photo)
async def handle_add_products(message: types.Message, state: FSMContext):
    os.makedirs(MEDIA_NEWSPAPER_DIR, exist_ok=True)
    for photo in message.photo[-1:]:
        
        file = await message.bot.get_file(photo.file_id)
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{photo.file_id}.jpg"
        file_path = os.path.join(MEDIA_NEWSPAPER_DIR, filename)
        await message.bot.download_file(file.file_path, file_path)
        
    markup = get_statistics()
    await message.answer('✅ Изрбражение успешно добавлено!', reply_markup=markup)
    await state.clear()