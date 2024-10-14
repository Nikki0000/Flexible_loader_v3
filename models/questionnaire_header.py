from sqlalchemy import Column, Integer, String,DateTime, Boolean
from sqlalchemy.orm import relationship
from .model_base import Base
from datetime import datetime

class QuestionnaireHeader(Base):
    __tablename__ = 'QuestionnaireHeader'
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(DateTime, default=datetime.utcnow, name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow, name='ModifiedOn')
    Name = Column(String, nullable=False, name='Name')
    Visible = Column(Boolean, default=True, name='Visible')
    Position = Column(Integer, nullable=False, name='Position')

    # configurations = relationship("QuestionConfiguration", back_populates="questionnaire_header")

    def __repr__(self):
        return f"<QuestionnaireHeader(Id={self.Id}, Name='{self.Name}')>"