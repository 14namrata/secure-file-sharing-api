from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import shutil
import os

from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.database import get_db
from app.models import Client, FileUpload

router = APIRouter(tags=["Ops"])  # Removed prefix to avoid /ops/ops routes

# ----------------------
# Schemas
# ----------------------
class AuthRequest(BaseModel):
    email: EmailStr
    password: str

# ----------------------
# Constants
# ----------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------------
# Ops Login
# ----------------------
@router.post("/ops/login")
def ops_login(data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(Client).filter_by(email=data.email, role="ops").first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email, "role": "ops"})
    return {"access_token": token, "token_type": "bearer"}

# ----------------------
# File Upload (Ops Only)
# ----------------------
@router.post("/ops/upload")
def upload_file(file: UploadFile = File(...), authorization: str = Header(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".pptx", ".docx", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only pptx, docx, and xlsx files are allowed")

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = FileUpload(filename=file.filename)
    db.add(new_file)
    db.commit()

    return {"message": "Upload successful", "filename": file.filename}
