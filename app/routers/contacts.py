from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, deps

router = APIRouter()

@router.post("/", response_model=schemas.ContactOut)
def create(contact: schemas.ContactCreate, db: Session = Depends(deps.get_db)):
    return crud.create_contact(db, contact)

@router.get("/", response_model=List[schemas.ContactOut])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_contacts(db, skip, limit)

@router.get("/search", response_model=List[schemas.ContactOut])
def search(query: str, db: Session = Depends(deps.get_db)):
    return crud.search_contacts(db, query)

@router.get("/upcoming_birthdays", response_model=List[schemas.ContactOut])
def birthdays(db: Session = Depends(deps.get_db)):
    return crud.upcoming_birthdays(db)

@router.get("/{contact_id}", response_model=schemas.ContactOut)
def read(contact_id: int, db: Session = Depends(deps.get_db)):
    db_contact = crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(deps.get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=schemas.ContactOut)
def delete(contact_id: int, db: Session = Depends(deps.get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact