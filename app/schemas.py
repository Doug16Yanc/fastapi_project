from typing import List
from pydantic import BaseModel
from enum import Enum

class CauseResponse(BaseModel):
    cause_id : int | None = None
    cause_name : str 
    description : str
    certification_code : str
    amount : float
    status_amount : str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ListCauseResponse(BaseModel):
        status : str
        results : int
        causes : List[CauseResponse]

class CauseCreate(BaseModel):
    cause_id: int
    cause_name: str
    description : str
    certification_code : str
    amount: float
    status_amount: str

    class Config:
        orm_mode = True

class StatusAmountEnum(str, Enum):
    STORED = 'stored'
    APPLIED = 'applied'


class CauseUpdate(BaseModel):
    status_amount: StatusAmountEnum

    class Config:
        orm_mode = True

class DonationResponse(BaseModel):
    donation_id : int | None = None 
    address_account : str  
    value : float
    fk_cause : int
  
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ListCauseResponse(BaseModel):
        status : str
        results : int
        causes : List[DonationResponse]

class DonationCreate(BaseModel):
    donation_id : int
    address_account : str 
    value: float
    fk_cause: int

    class Config:
        orm_mode = True 