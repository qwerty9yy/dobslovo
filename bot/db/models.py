from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)

"""Объяснение:

ORM-модель User — это таблица пользователей.

tg_id уникален — нельзя дважды зарегистрировать одного Telegram-пользователя.

username необязателен — не все пользователи имеют username.

Base используется для регистрации всех моделей (если их будет больше)."""