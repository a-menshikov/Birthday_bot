from config import SUB_KIND
from data.db_loader import Base, db_session, engine
from data.models import Subscribe
from data.services import input_c_birthdays_in_base


async def create_db():
    """Создание БД и наполнение ее предустановленными данными."""
    Base.metadata.create_all(engine)
    session = db_session()
    for i in SUB_KIND.items():
        check = session.query(Subscribe).filter(Subscribe.name == i[0]).all()
        if not check:
            private_subscribe = Subscribe(
                name=i[0],
                comment=i[1]
            )
            session.add(private_subscribe)
            session.commit()
    await input_c_birthdays_in_base()
