from fastapi import FastAPI
from app.routers import contacts
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])