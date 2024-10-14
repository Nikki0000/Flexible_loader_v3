# Создаем базу для всех моделей с помощью declarative_base
# Определяем функции для создания соединения с базой данных и получения сессии


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_engine(db_url):
    return create_engine(db_url)

def get_session(engine):
    return sessionmaker(bind=engine)