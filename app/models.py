# app/models.py
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.sql import func # Додайте цей імпорт
from sqlalchemy.orm import relationship # Додайте цей імпорт
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)
    # Додамо user_id для зв'язку з користувачем
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="contacts") # Додайте цей імпорт і relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    confirmed = Column(Boolean, default=False)
    contacts = relationship("Contact", back_populates="user") # Додайте цей імпорт і relationship
    avatar_url = Column(String, nullable=True)