from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app import deps, crud, models, schemas
from app.auth import get_current_user
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/users", tags=["Users"])

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

try:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )
    print("Cloudinary configuration successful (or at least no immediate error).")
except Exception as e:
    print(f"Error configuring Cloudinary: {e}")

@router.patch("/avatar", response_model=schemas.UserOut)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(deps.get_db)
):
    print(f"Attempting to upload avatar for user ID: {current_user.id}")
    try:
        r = cloudinary.uploader.upload(file.file, folder="avatars", public_id=f"avatar_{current_user.id}", overwrite=True)
        avatar_url = r.get("secure_url")
        print(f"Cloudinary upload result: {r}")
        print(f"New avatar URL: {avatar_url}")

        user = crud.get_user_by_email(db, email=current_user.email)
        if user:
            user.avatar_url = avatar_url
            db.commit()
            db.refresh(user)
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except cloudinary.exceptions.Error as ce:
        print(f"Cloudinary API Error: {ce}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Cloudinary upload failed: {ce}")
    except Exception as e:
        print(f"An unexpected error occurred during avatar upload: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")