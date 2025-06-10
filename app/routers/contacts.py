# app/routers/contacts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, deps, models
from app.auth import get_current_user # Імпортуємо функцію для отримання поточного користувача

router = APIRouter()

@router.post("/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create(
    contact: schemas.ContactCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user) # Залежність від аутентифікованого користувача
):
    # Додаємо user_id до нового контакту
    return crud.create_contact(db, contact, user_id=current_user.id) # Потрібно оновити crud.create_contact

@router.get("/", response_model=List[schemas.ContactOut])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Фільтруємо контакти за user_id
    return crud.get_contacts(db, skip, limit, user_id=current_user.id) # Потрібно оновити crud.get_contacts

@router.get("/search", response_model=List[schemas.ContactOut])
def search(
    query: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Фільтруємо контакти за user_id
    return crud.search_contacts(db, query, user_id=current_user.id) # Потрібно оновити crud.search_contacts

@router.get("/upcoming_birthdays", response_model=List[schemas.ContactOut])
def birthdays(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Фільтруємо контакти за user_id
    return crud.upcoming_birthdays(db, user_id=current_user.id) # Потрібно оновити crud.upcoming_birthdays

@router.get("/{contact_id}", response_model=schemas.ContactOut)
def read(
    contact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = crud.get_contact(db, contact_id, user_id=current_user.id) # Потрібно оновити crud.get_contact
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    # Перевірка належності контакту користувачу
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this contact")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = crud.get_contact(db, contact_id, user_id=current_user.id) # Потрібно оновити crud.get_contact
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this contact")
    return crud.update_contact(db, contact_id, contact)

@router.delete("/{contact_id}", response_model=schemas.ContactOut)
def delete(
    contact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_contact = crud.get_contact(db, contact_id, user_id=current_user.id) # Потрібно оновити crud.get_contact
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this contact")
    return crud.delete_contact(db, contact_id)