from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .model_base import Base
from datetime import datetime

class QuestionAnswer(Base):
    __tablename__ = 'QuestionAnswer'
    Id = Column(Integer, primary_key=True)
    QuestionId = Column(Integer, ForeignKey('Question.Id'), nullable=False)
    Order = Column(Integer, nullable=False)
    CreatedOn = Column(DateTime, default=datetime.utcnow, name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow, name='ModifiedOn')
    Name = Column(String, nullable=False)