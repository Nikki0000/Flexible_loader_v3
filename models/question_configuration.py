from sqlalchemy import Column, Integer, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from .model_base import Base
from datetime import datetime

class QuestionConfiguration(Base):
    __tablename__ = 'QuestionConfiguration'
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(DateTime, default=datetime.utcnow, name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow, name='ModifiedOn')
    QuestionId = Column(Integer, ForeignKey('Question.Id'), nullable=False, name='QuestionId')
    QuestionnaireHeaderId = Column(Integer, ForeignKey('QuestionnaireHeader.Id'), nullable=False, name='QuestionnaireHeaderId')
    RowNumber = Column(Integer, nullable=False, name='RowNumber')
