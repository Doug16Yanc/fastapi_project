from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

router = APIRouter()

def convert_ether_in_dollar(value : float):
    return value * 3664.03

@router.post('/donations', status_code=status.HTTP_201_CREATED)
def create_donation(payload: schemas.DonationCreate, db: Session = Depends(get_db)):
    cause = db.query(models.Cause).filter(models.Cause.cause_id == payload.fk_cause).first()
    if not cause:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cause does not exist.")
    
    donation_in_dollars = convert_ether_in_dollar(payload.value)

    new_donation = models.Donation(**payload.dict()) 
    if cause.status_amount == "stored" :
        try:
            cause.amount += donation_in_dollars
            db.add(new_donation)
            db.commit()
            db.refresh(new_donation)
            return {"status": "success", "message" : "Donation created successfully!", "donation": new_donation}
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
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The cause can only receive the donated amount if " +
                                                                            "it has not yet applied any of its stored amount.")

@router.get('/donations/{donation_id}')
def get_donation_by_id(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(models.Donation).filter(models.Donation.donation_id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return {"status": "success", "donation": donation}

@router.get('/donations')
def get_donations(db : Session = Depends(get_db)):
    donations = db.query(models.Donation).all()
    if not donations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No donations found")
    return {"status": "success", "message": "Donations found successfully!", "data": donations}


@router.patch('/donations/{donation_id}')
def update_donation(donation_id: int, payload: schemas.DonationCreate, db: Session = Depends(get_db)):
    donation_query = db.query(models.Donation).filter(models.Donation.donation_id == donation_id)
    db_donation = donation_query.first()

    if not db_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

    update_data = payload.dict(exclude_unset=True)
    donation_query.update(update_data, synchronize_session=False)
    
    try:
        db.commit()
        db.refresh(db_donation)
        return {"status": "success", "donation": db_donation}
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

@router.delete('/donations/{donation_id}')
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    donation_query = db.query(models.Donation).filter(models.Donation.donation_id == donation_id)
    db_donation = donation_query.first()

    if not db_donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

    donation_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "message": "Donation deleted successfully.", "data": donation_query}
