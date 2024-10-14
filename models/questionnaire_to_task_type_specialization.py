from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .model_base import Base

class QuestionnaireToTaskTypeSpecialization(Base):
    __tablename__ = 'QuestionnaireToTaskTypeSpecialization'
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(DateTime, default=datetime.utcnow(), name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow(), name='ModifiedOn')
    QuestionnaireId = Column(Integer, ForeignKey('Questionnaire.Id'), nullable=False)
    SpecializationId = Column(Integer, nullable=False)
    QuestionnaireToTaskTypeId = Column(Integer, ForeignKey('QuestionnaireToTaskType.Id'), nullable=False)
