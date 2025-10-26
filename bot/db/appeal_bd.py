from sqlite3 import IntegrityError
from sqlalchemy import select, func
from typing import List
from bot.db.base import async_session_maker
from bot.db.models import User, SentPost

async def get_user_count() -> int:
    """Подсчет количества пользователей"""
    async with async_session_maker() as session:
        result = await session.execute(select(func.count(User.id)))
        return result.scalar() or 0
    
async def get_all_users_tg_id() -> List[int]:
    """Получить все tg_id пользователей"""
    async with async_session_maker() as session:
        result = await session.execute(select(User.tg_id))
        return result.scalars().all()
    
# Получаем всех пользователей
async def get_all_user():
    async with async_session_maker() as session:
        resuilt = await session.execute(select(User))
        return resuilt.scalars().all()
    
# Проверяем — был ли уже этот пост отправлен
async def is_post_sent(channel_id: int, message_id: int) -> bool:
    async with async_session_maker() as session:
        result = await session.execute(
            select(SentPost).where(
                SentPost.channel_id == channel_id,
                SentPost.message_id == message_id
            )
        )
        return result.scalar_one_or_none() is not None
    
# Сохраняем информацию о рассылке
async def mark_post_as_sent(channel_id: int, message_id: int):
    async with async_session_maker() as session:
        session.add(SentPost(channel_id=channel_id, message_id=message_id))
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()  # уже был