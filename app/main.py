from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import random, string

app = FastAPI()

class Status(Enum):
    APPLIED = "applied"
    STORED = "stored"


class Cause(BaseModel) :
    cause_id : int
    cause_name: str
    description : str
    certification_code : str
    amount : float 
    status_amount : Status 

class Donation(BaseModel) :
    donation_id : int
    address_account : str
    cause_id : int
    value : float
    
causes = []
donations = []


@app.post("/causes", status_code=201)
async def create_cause(cause : Cause):
    if any (sake["cause_id"] == cause["cause_id"] for sake in causes):
        raise HTTPException(status_code=400, detail="Cause already exists.")

    causes.append(cause)

    return {
        "status" : "Success",
        "message" : "Cause created successfully!",
        "data" : cause
    }

@app.get("/causes/{cause_id}", status_code = 200)
async def get_cause_by_id(cause_id : int):
    if causes:
        for cause in causes:
            if cause.cause_id == cause_id:
                return {
                    "status" : "Success",
                    "message" : "Cause found successfully!",
                    "data" : cause
                }
            raise HTTPException(status_code=404, detail="Cause not found")
    raise HTTPException(status_code=404, detail="The list is empty.")

@app.get("/causes", status_code=200)
async def get_causes():
    if causes:
        return {
            "status" : "Success",
            "message" : "Cause found successfully!",
            "data" : causes
        }
    raise HTTPException(status_code=404, detail="The list is empty.")


#Apenas o status do montante doado à causa pode ser atualizado se e somente se 
#a causa tiver recebido alguma doação.
@app.put("/causes/{cause_id}", status_code=200)
async def update_cause_by_id(cause_id : int):
    for cause in causes:
        if cause.cause_id == cause_id and cause.amount > 0.0: 
            if cause.status_amount == Status.STORED:
                cause.status_amount = Status.APPLIED

                return {
                    "message" : "Status updated successfully.",
                    "cause" : cause
                }
            else:
                raise HTTPException(status_code=400, detail="Just only status can be updated.")

        raise HTTPException(status_code=404, detail="Cause not found or no donations registered yet")
    raise HTTPException(status_code=404, detail="The list is empty.")
    
   


@app.delete("/causes/{cause_id}", status_code=200)
async def delete_cause_by_id(cause_id : int):
    if causes:
        for cause in causes:
            if cause.cause_id == cause_id and cause.status_amount == Status.APPLIED:
                index = causes.index(cause)  
                cause_deleted = causes.pop(index)
                return {
                    "status": "Success",
                    "message": "Cause deleted successfully.",
                    "data": cause_deleted
                 }
            raise HTTPException(status_code=404, detail="Cause not found or amount not applied yet.")
    raise HTTPException(status_code=400, detail="The list is empty.")



#Cria um hash para as transações
def create_transaction_hash():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))

#Converte a doação realizada na criptomoeda da Ethereum em dólar americano
def convert_ether_in_dollar(value : float):
    return value * 3664.03

@app.post("/donations", status_code=200)
async def create_donation(donation : Donation):

    cause = next((grant for grant in causes if grant.cause_id == donation.cause_id), None)
    
    if cause is None:
        raise HTTPException(status_code=400, detail="Cause does not exist.")

    transaction_hash = create_transaction_hash()

    donation_dollar = convert_ether_in_dollar(donation.value)

    cause.amount += donation_dollar

    donations.append(donation)

    return {
        "status" : "Success",
        "message" : "Donation processed successfully!",
        "data" : {
            "donation" :donation,
            "transaction_hash" : transaction_hash 
        }
    }


@app.get("/donations/{donation_id}", status_code = 200)
async def get_donation_by_id(donation_id : int):
    if donations:
        for donation in donations:
            if donation.donation_id == donation_id:
                return {
                    "status" : "Success",
                    "message" : "Donation processed successfully!",
                    "data" : donation
                }
            raise HTTPException(status_code=404, detail="Donation not found.")

    raise HTTPException(status_code=404, detail="The list is empty.")

@app.get("/donations", status_code=200)
async def get_donations():
    if donations:
        return {
            "status" : "Success",
            "message" : "Donations processed successfully!",
            "data" : donations
        }
    raise HTTPException(status_code=404, detail="The list is empty.")


@app.delete("/donations/{donation_id}", status_code=200)
async def delete_donation_by_id(donation_id : int):
    if donations:
        for donation in donations:
            if donation.donation_id == donation_id:
                index = donations.index(donation)
                donation_deleted = donations.pop(index)
                return {
                    "status" : "Success",
                    "message" : "Donation deleted successfully, but the value of the transactions remains in Ethereum.",
                    "data" : donation_deleted
                }
            raise HTTPException(status_code=404, detail="Donation not found.")
    raise HTTPException(status_code=404, detail="The list is empty.")