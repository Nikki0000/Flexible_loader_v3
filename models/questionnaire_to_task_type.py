from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .model_base import Base


class QuestionnaireToTaskType(Base):
    __tablename__ = 'QuestionnaireToTaskType'
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(DateTime, default=datetime.utcnow, name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow, name='ModifiedOn')
    QuestionnaireId = Column(Integer, ForeignKey('Questionnaire.Id'), nullable=False)
    TaskTypeId = Column(Integer, nullable=False)
    Order = Column(Integer, nullable=False)