# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import datetime, timedelta
from app import models, schemas

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    # Додаємо user_id до створення контакту
    db_contact = models.Contact(**contact.dict(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(models.Contact)
    if user_id:
        query = query.filter(models.Contact.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, user_id: int = None):
    query = db.query(models.Contact).filter(models.Contact.id == contact_id)
    if user_id:
        query = query.filter(models.Contact.user_id == user_id)
    return query.first()

def update_contact(db: Session, contact_id: int, updates: schemas.ContactUpdate, user_id: int = None):
    db_contact = get_contact(db, contact_id, user_id)
    if db_contact:
        # Перевірка належності контакту перед оновленням
        if user_id and db_contact.user_id != user_id:
            return None # Або викликати HTTPException тут, якщо хочете
        for field, value in updates.dict().items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int = None):
    db_contact = get_contact(db, contact_id, user_id)
    if db_contact:
        # Перевірка належності контакту перед видаленням
        if user_id and db_contact.user_id != user_id:
            return None # Або викликати HTTPException тут
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str, user_id: int = None):
    filters = or_(
        models.Contact.first_name.ilike(f"%{query}%"),
        models.Contact.last_name.ilike(f"%{query}%"),
        models.Contact.email.ilike(f"%{query}%")
    )
    if user_id:
        return db.query(models.Contact).filter(filters, models.Contact.user_id == user_id).all()
    return db.query(models.Contact).filter(filters).all()

def upcoming_birthdays(db: Session, user_id: int = None):
    today = datetime.today().date()
    upcoming = today + timedelta(days=7)

    query = db.query(models.Contact)
    if user_id:
        query = query.filter(models.Contact.user_id == user_id)
    contacts = query.all()
    result = []

    for contact in contacts:
        bday_this_year = contact.birthday.replace(year=today.year)
        if today <= bday_this_year <= upcoming:
            result.append(contact)

    return result