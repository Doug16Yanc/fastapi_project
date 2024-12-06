from typing import List
from pydantic import BaseModel

class CauseBaseSchema(BaseModel):
    cause_id : int | None = None
    cause_name : str 
    description : str
    certification_code : str
    amount : float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ListCauseResponse(BaseModel):
        status : str
        results : int
        causes : List[CauseBaseSchema]

class DonationBaseSchema(BaseModel):
    donation_id : int | None = None 
    address_account : str
    cause_id : int
    value : float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class ListCauseResponse(BaseModel):
        status : str
        results : int
        causes : List[DonationBaseSchema]