from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import config

engine = create_async_engine(url=config.database_url)
session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
