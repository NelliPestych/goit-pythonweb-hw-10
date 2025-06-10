# app/routers/users.py (або розширте auth.py)
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app import deps, crud, models, schemas
from app.auth import get_current_user
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/users", tags=["Users"]) # Новий роутер для користувачів

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

@router.patch("/avatar", response_model=schemas.UserOut)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    r = cloudinary.uploader.upload(file.file, folder="avatars", public_id=f"avatar_{current_user.id}", overwrite=True)
    avatar_url = r.get("secure_url")

    user = crud.get_user_by_email(db, email=current_user.email)
    if user:
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
        return user
    raise HTTPException(status_code=404, detail="User not found")