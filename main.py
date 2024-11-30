from fastapi import FastAPI, Form, HTTPException, Query
from pydantic import BaseModel
import random
import string


app = FastAPI()

causes = []
donations = [] 

class Cause(BaseModel) :
    cause_id : int
    cause_name: str
    description : str
    certification_code : str
    amount : float

class Donation(BaseModel) :
    cause_id : int
    value : float


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
    for cause in causes:
        if cause.cause_id == cause_id:
            return {
                "status" : "Success",
                "message" : "Cause found successfully!",
                "data" : cause
            }
        raise HTTPException(status_code=404, detail="Cause not found")

@app.get("/causes", status_code=200)
async def get_causes():
    if causes:
        return {
            "status" : "Success",
            "message" : "Cause found successfully!",
            "data" : causes
        }
    raise HTTPException(status_code=401, detail="The list is empty.")

@app.get("/causes{cause_id}", status_code=200)
async def delete_cause_by_id(cause_id : id):
    if causes:
        for cause in causes:
            if cause["cause_id"] == cause_id and cause["amount"] > 0.0:
                return "The amount of this cause is $ " + cause["amount"]
                cause_deleted = causes.pop(cause)
                return {
                    "status": "success",
                    "message": "Student deleted successfully.",
                    "data": cause_deleted
                 }
            raise HTTPException(status_code=404, detail="Cause not found.")
    raise HTTPException(status_code=400, detail="The list is empty.")


#Cria um hash para as transações
def create_transaction_hash():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))

#Converte a doação realizada na criptomoeda da Ethereum em dólar americano
def convert_ether_in_dollar(value : float):
    return value * 3664.03

@app.post("/donations", status_code=200)
async def create_donation(donation : Donation):

    cause = next((sake for sake in causes if sake.cause_id == donation.cause_id), None)
    
    if cause is None:
        raise HTTPException(status_code=400, detail="Cause does not exist.")

    transaction_hash = create_transaction_hash()

    donation_dollar = convert_ether_in_dollar(donation.value)

    cause.amount += donation_dollar

    donations.append({
        "cause_id" : cause.cause_id,
        "donation_id" : transaction_hash,
        "donation" : donation_dollar
    })

    return {
        "status" : "Success",
        "message" : "Donation processed successfully!",
        "data" : {
            "donation" :donation,
            "transaction_hash" : transaction_hash 
        }
    }
