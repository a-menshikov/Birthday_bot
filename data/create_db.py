from data.db_loader import Base, db_session, engine
from data.models import Subscribe
from data.services import input_c_birthdays_in_base


async def create_db():
    """Создание БД и наполнение ее предустановленными данными."""
    Base.metadata.create_all(engine)
    session = db_session()
    check = session.query(Subscribe).filter(Subscribe.name == 'private').all()
    if not check:
        private_subscribe = Subscribe(name='private',
                                      comment=('добавленные пользователем'
                                               ' дни рождения')
                                      )
        session.add(private_subscribe)
        session.commit()
    await input_c_birthdays_in_base()
