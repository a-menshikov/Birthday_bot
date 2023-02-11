from datetime import date

from .db_loader import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class User(Base):
    """Модель пользователя."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    created_on = Column(Text, default=date.today)
    active = Column(Integer, nullable=False, default=1)
    notes = relationship('Birthday', backref="notes")


class Birthday(Base):
    """Запись о дне рождения."""
    __tablename__ = 'birthdays'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Text, nullable=False)
    row_birth_date = Column(Text, nullable=False)
    day_of_birth = Column(Integer, nullable=False)
    month_of_birth = Column(Integer, nullable=False)
    comment = Column(Text)
    created_on = Column(Text, default=date.today)


class Birthday_CF(Base):
    """Запись о дне рождения для списка Ц."""
    __tablename__ = 'birthdays_cf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    row_birth_date = Column(Text, nullable=False)
    day_of_birth = Column(Integer, nullable=False)
    month_of_birth = Column(Integer, nullable=False)
    year_of_birth = Column(Integer, nullable=False)
    division = Column(Text)
    position = Column(Text)
    created_on = Column(Text, default=date.today)


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
