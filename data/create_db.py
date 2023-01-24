from .db_loader import Base, db_session, engine
from .models import Subscribe


def create_db():
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
