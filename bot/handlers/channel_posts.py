import asyncio
from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from bot.utils.logger import logger

from bot.db.appeal_bd import get_all_users_tg_id, is_post_sent, mark_post_as_sent

router = Router()
# Временное хранилище альбомов
media_groups = {}
# Чтобы отслеживать, какие группы уже обрабатываются
processing_groups = set()

"""
Канал: [Фото1] → [Фото2] → [Фото3]  (альбом)
          ↓         ↓         ↓
Бот:   собирает в media_groups[abc123] = [Фото1, Фото2, Фото3]
          ↓
       ждет 3 секунды
          ↓
       отправляет send_media_group([Фото1, Фото2, Фото3])
          ↓
Пользователь: получает один альбом с тремя фото
"""
     


@router.channel_post()
async def channel_post_handler(message: Message):
    """Ловим новые посты из канала."""
    channel_id = message.chat.id
    message_id = message.message_id
    media_group_id = message.media_group_id
    
    logger.info(f"📢 Новый пост в канале {message.chat.title}, MediaGroup: {media_group_id}")

    # Если это альбом (медиагруппа)
    if media_group_id:
        await handle_media_group(message, channel_id, media_group_id)
    else:
        # Обычный пост (не альбом)
        await handle_single_message(message, channel_id, message_id)

async def handle_media_group(message: Message, channel_id: int, media_group_id: str):
    """Обрабатываем медиагруппу"""
    # Добавляем сообщение в группу
    if media_group_id not in media_groups:
        media_groups[media_group_id] = []
    media_groups[media_group_id].append(message)
    
    # print(f"📦 Добавлен элемент в группу {media_group_id}. Всего: {len(media_groups[media_group_id])}")
    
    # Если группа уже обрабатывается - выходим
    if media_group_id in processing_groups:
        return
        
    # Помечаем группу как обрабатываемую
    processing_groups.add(media_group_id)
    
    # Ждём 3 секунды, чтобы собрать ВСЕ элементы альбома
    await asyncio.sleep(3.0)
    
    # Получаем финальную группу (после ожидания)
    final_group = media_groups.get(media_group_id, [])
    
    if not final_group:
        processing_groups.discard(media_group_id)
        return
    
    # Проверяем, не отправили ли уже эту группу
    if await is_post_sent(channel_id, media_group_id):
        # print(f"⚠️ Группа {media_group_id} уже отправлена")
        # Очищаем
        media_groups.pop(media_group_id, None)
        processing_groups.discard(media_group_id)
        return
    
    # print(f"🎯 Начинаем рассылку группы {media_group_id} из {len(final_group)} элементов")
    
    # Создаем медиагруппу для отправки
    media = []
    for idx, m in enumerate(final_group):
        # Подпись только у первого элемента
        caption = m.caption if idx == 0 else None
        
        if m.photo:
            media.append(InputMediaPhoto(
                media=m.photo[-1].file_id, 
                caption=caption
            ))
            # print(f"  📷 Добавлено фото {idx + 1}")
        elif m.video:
            media.append(InputMediaVideo(
                media=m.video.file_id, 
                caption=caption
            ))
            # print(f"  🎥 Добавлено видео {idx + 1}")
        elif m.document:
            media.append(InputMediaDocument(
                media=m.document.file_id, 
                caption=caption
            ))
            # print(f"  📄 Добавлен документ {idx + 1}")
    
    # Получаем пользователей
    users = await get_all_users_tg_id()
    if not users:
        # print("⚠️ Нет пользователей для рассылки.")
        # Очищаем
        media_groups.pop(media_group_id, None)
        processing_groups.discard(media_group_id)
        return
    
    # Отправляем всем пользователям
    success_count = 0
    for user in users:
        try:
            await message.bot.send_media_group(chat_id=user, media=media)
            success_count += 1
            await asyncio.sleep(0.1)  # Небольшая задержка между отправками
        except Exception as e:
            logger.error(f"❌ Ошибка отправки альбома пользователю {user}: {e}", exc_info=True)
    
    # Помечаем группу как отправленную
    await mark_post_as_sent(channel_id, media_group_id)
    logger.info(f"✅ Группа из {len(media)} элементов отправлена {success_count}/{len(users)} пользователям")
    
    # Очищаем
    media_groups.pop(media_group_id, None)
    processing_groups.discard(media_group_id)

async def handle_single_message(message: Message, channel_id: int, message_id: int):
    """Обрабатываем одиночное сообщение"""
    if await is_post_sent(channel_id, message_id):
        # print(f"⚠️ Пост {message_id} уже отправлен")
        return
    
    users = await get_all_users_tg_id()
    if not users:
        # print("⚠️ Нет пользователей для рассылки.")
        return
    
    success_count = 0
    for user in users:
        try:
            await message.copy_to(user)
            success_count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"❌ Ошибка копирования пользователю {user}: {e}", exc_info=True)

    await mark_post_as_sent(channel_id, message_id)
    logger.info(f"✅ Одиночный пост отправлен {success_count}/{len(users)} пользователям")


     
                
# @router.channel_post()
# async def channel_post_handler(message: Message):
#     # """Ловим новые посты из канала."""
#     # channel_id = message.chat.id
#     # message_id = message.message_id
    
#     # # Проверяем — не отправляли ли уже этот пост
#     # if await is_post_sent(channel_id, message_id):
#     #     print(f"⚠️ Пост {message_id} уже был отправлен — пропускаем.")
#     #     return
    
#     print(f"📢 Новый пост в канале {message.chat.title}")
    
#     users = await get_all_users_tg_id()
#     if not users:
#         print("⚠️ Нет пользователей для рассылки.")
#         return

#     for user in users:
#         try:
#             await message.copy_to(user)
#             await asyncio.sleep(0.5)
#         except Exception as e:
#             print(f"❌ Ошибка копирования {user}: {e}")

#     # # Помечаем пост как отправленный
#     # await mark_post_as_sent(channel_id, message_id)
#     print("✅ Рассылка завершена.")
                