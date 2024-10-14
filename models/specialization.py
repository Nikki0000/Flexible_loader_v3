from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from .model_base import Base

class Specialization(Base):
    __tablename__ = 'Specialization'
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(DateTime, default=datetime.utcnow(), name='CreatedOn')
    ModifiedOn = Column(DateTime, default=datetime.utcnow(), name='ModifiedOn')
    Name = Column(String, nullable=False)