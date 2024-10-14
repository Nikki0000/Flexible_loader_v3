# Определяем модель TaskType, представляющую тип задачи с полями Id и Name
# Используем SQLAlchemy для описания структуры таблицы и ее атрибутов


from sqlalchemy import Column, Integer, String
from .model_base import Base

class TaskType(Base):
    __tablename__ = 'TaskType' # Таблица из БД

    Id = Column(Integer, primary_key=True) # Устанавливаем первичный ключ таблицы TaskType
    Name = Column(String, nullable=False) # Название TaskType

    def __repr__(self):
        return f"<TaskType(Id={self.Id}, Name='{self.Name}')>"