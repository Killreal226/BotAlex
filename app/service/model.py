from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=True)
    experience = Column(String(32), nullable=True)
    riding_style = Column(String(32), nullable=True)
    purpose = Column(String(256), nullable=True)
    preferences = Column(String(256), nullable=True)
    response_gpt = Column(Text, nullable=True)
    id_user_telegram = Column(String(64), nullable=True)
