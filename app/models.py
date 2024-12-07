from .database import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
#from fastapi_utils.guid_type
from enum import Enum

class Status_Amount(Enum):
    STORED = 'stored'
    APPLIED = 'applied'


class Cause(Base) :
    __tablename__ = 'causes'
    cause_id = Column(Integer, primary_key=True)
    cause_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    certification_code = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status_amount = Column(String, default=Status_Amount.STORED)


class Donation(Base) :
    __tablename__ = 'donations'
    donation_id = Column(Integer, primary_key=True)
    address_account = Column(String, nullable=False) 
    value = Column(Float, nullable=False)
    fk_cause = Column(Integer, ForeignKey('causes.cause_id'), nullable=False)
    cause = relationship('Cause', backref='donations')
