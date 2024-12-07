from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

router = APIRouter()

@router.post('/causes', status_code=status.HTTP_201_CREATED)
def create_cause(payload: schemas.CauseCreate, db: Session = Depends(get_db)):
    existing_cause = db.query(models.Cause).filter(models.Cause.cause_id == payload.cause_id).first()
    if existing_cause:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cause already exists.")

    new_cause = models.Cause(**payload.dict())  
    try:
        db.add(new_cause)
        db.commit()
        db.refresh(new_cause)
        return {"status": "success", "message": "Cause created successfully!", "data": new_cause}
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A database integrity error occurred. Please verify your data."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )

@router.get('/causes/{cause_id}')
def get_cause_by_id(cause_id: int, db: Session = Depends(get_db)):
    cause = db.query(models.Cause).filter(models.Cause.cause_id == cause_id).first()
    if not cause:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cause not found")
    return {"status": "success", "message": "Cause found successfully!", "data": cause}

@router.get('/causes')
def get_causes(db: Session = Depends(get_db)):
    causes = db.query(models.Cause).all()
    if not causes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No causes found")
    return {"status": "success", "message": "Causes found successfully!", "data": causes}


@router.patch('/causes/{cause_id}')
def update_cause_by_id(cause_id: int, payload: schemas.CauseUpdate, db: Session = Depends(get_db)):
    cause_db = db.query(models.Cause).filter(models.Cause.cause_id == cause_id).first()
    causes = db.query(models.Cause).all()
    
    if not cause_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cause not found")
    
    if cause_db.amount <= 0.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No donations registered yet")
    
    if cause_db.status_amount == "stored":
        cause_db.status_amount = payload.status_amount
        
        try:
            db.commit()
            db.refresh(cause_db)
            return {"status": "success", "message": "Status updated successfully.", "cause": cause_db}
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A database integrity error occurred. Please verify your data."
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred. {e}"
            )
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Just only status can be updated.")


@router.delete('/causes/{cause_id}')
def delete_cause_by_id(cause_id: int, db: Session = Depends(get_db)):
    cause = db.query(models.Cause).filter(models.Cause.cause_id == cause_id).first()
    if not cause:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cause not found")
    
    if cause.status_amount != "applied":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount not applied yet.")

    try:
        db.delete(cause)
        db.commit()
    except IntegrityError:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cause cannot be deleted as it has associated donations."
        )

    return {"status": "success", "message": "Cause deleted successfully.", "data": cause}
