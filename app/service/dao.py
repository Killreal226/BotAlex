from app.base_dao import BaseDAO
from app.service.model import User


class UserDAO(BaseDAO):
    model = User
