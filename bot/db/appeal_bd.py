from sqlalchemy import select, func
from typing import List
from bot.db.base import async_session_maker
from bot.db.models import User

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