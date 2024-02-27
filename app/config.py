import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/config.env")

    DB_HOST: str  # localhost или IP сервера
    DB_PORT: int  # Порт 3306 по дефолту
    DB_USERNAME: str  # Имя юзернейма, дефолтное root
    DB_PASSWORD: str  # Пароль
    DB_NAME: str  # Имя базы данных (если используется локальная, то путь толжен быть /data/config/)

    LOG_FILE: str  # Путь к файлу для записи логов

    BOT_TOKEN: str  # Токен, выдаваемый при регистрации бота в telegram
    OPENAI_TOKEN: str  # Токен openai

    DATA_MESSAGES: dict = {}  # Словарь с сообщениями и шаблонами сообщений

    @property
    def database_url(self):
        """Создание ссылки на подключение к БД"""
        return f"mysql+aiomysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def load_data_messages(self, path="./config/data_messages.json"):
        with open(path, "r", encoding="utf-8") as f:
            self.DATA_MESSAGES = json.load(f)


config = Config()
config.load_data_messages()
