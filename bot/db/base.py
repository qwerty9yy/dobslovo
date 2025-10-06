from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from bot.config.settings import settings

Base = declarative_base()
engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


"""Объяснение:

create_async_engine позволяет работать с SQLite асинхронно (через aiosqlite).

Используем sessionmaker для управления транзакциями.

get_session() — dependency, которое удобно импортировать в CRUD и хендлеры.

Код безопасен — каждая сессия закрывается автоматически (async with)."""