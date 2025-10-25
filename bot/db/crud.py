import select
from bot.db.models import User
from sqlalchemy import select
from bot.db.base import async_session_maker
from sqlalchemy.exc import IntegrityError

async def add_user(tg_id: int, username: str | None = None):
    async with async_session_maker() as session:
        user = User(tg_id=tg_id, username=username)
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            # Можно просто проигнорировать или вернуть существующего юзера
            return None

async def get_user_by_tg_id(tg_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()



"""Объяснение:

CRUD (Create, Read, Update, Delete) слой изолирует работу с БД от логики бота.

Если пользователь новый — создаем его.

Это позволяет переиспользовать код (например, в других хендлерах)."""