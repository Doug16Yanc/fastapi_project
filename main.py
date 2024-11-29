from fastapi import FastAPI, Form, HTTPException, Query


app = FastAPI()

causes = []
donations = [] 

@app.post("/causes", status = 201)
async def create_cause(cause : dict):
    if any (sake["id"] == cause["id"] for sake in causes):
        raise HTTPException(status_code=400, detail="Cause already exists.")

    cause["amount"] = 0.0
    causes.append(cause)

    return {
        "status" : "Success",
        "message" : "Cause created successfully!",
        "data" : cause
    }

@app.get("/causes/{id}", status = 200)
async def get_cause_by_id(cause_id : int):
    for cause in causes:
        if cause["id"] == id:
            return {
                "status" : "Success",
                "message" : "Cause found successfully!",
                "data" : cause
            }
        raise HTTPException(status_code=404, detail="Cause not found")

@app.get("/causes", status=200)
async def get_causes(cause : dict):
    if causes:
        for cause in causes:
            return {
                "status" : "Success",
                "message" : "Cause found successfully!",
                "data" : cause
            }
    raise HTTPException(status_code=401, detail="The list is empty.")

@app.get("/causes{id}", status=200)
async def delete_cause_by_id(cause_id : id):
    if causes:
        for cause in causes:
            if cause["id"] == id and cause["amount"] > 0.0:
                return "The amount of this cause is $ " + cause["amount"]
                cause_deleted = causes.pop(cause)
                return {
                    "status": "success",
                    "message": "Student deleted successfully.",
                    "data": cause_deleted
                 }
            raise HTTPException(status_code=404, detail="Cause not found.")
    raise HTTPException(status_code=400, detail="The list is empty.")