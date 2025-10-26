from sqlalchemy import Column, Integer, BigInteger, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SentPost(Base):
    __tablename__ = 'sent_posts'
    
    id = Column(Integer, primary_key= True)
    channel_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, unique=True, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    

"""Объяснение:

ORM-модель User — это таблица пользователей.

tg_id уникален — нельзя дважды зарегистрировать одного Telegram-пользователя.

username необязателен — не все пользователи имеют username.

Base используется для регистрации всех моделей (если их будет больше)."""