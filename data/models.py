from datetime import date

from .db_loader import Base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(Integer(), nullable=False, unique=True)
    created_on = Column(Date(), default=date.today)
    active = Column(Integer(), nullable=False, default=1)
    notes = relationship('Birthday', backref="notes")


class Birthday(Base):
    """Запись о дне рождения."""
    __tablename__ = 'birthdays'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(200), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    created_on = Column(Date(), default=date.today)


class Subscribe(Base):
    """Тип подписки на рассылку."""
    __tablename__ = 'subscribe_kind'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    comment = Column(Text, nullable=False)


class UserSubscribe(Base):
    """Подписки пользователя."""
    __tablename__ = 'users_subcribe'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subscribe = Column(Integer, ForeignKey('subscribe_kind.id'))
    status = Column(Boolean, nullable=False)
