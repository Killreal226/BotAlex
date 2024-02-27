from loguru import logger
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from app.database import session


class BaseDAO:
    model = None

    @classmethod
    async def add_one(cls, **kwargs) -> None:
        """
        Вставка в таблицу одной новой записи. \n
        **Пример вызова функции:**
        await test_1.add_one(name='Kirill', surname ='Kazakov')
        """
        async with session() as sess:
            try:
                query = insert(cls.model).values(kwargs)
                await sess.execute(query)
                await sess.commit()
            except IntegrityError as e:
                await sess.rollback()
                logger.info(f"error in add_one: {e}")
