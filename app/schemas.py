from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

# ------------------------------
# Auth Models
# ------------------------------

class LoginData(BaseModel):
    email: EmailStr
    password: str

class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ------------------------------
# File Metadata / Download
# ------------------------------

class FileResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime

    class Config:
        orm_mode = True

class FileListResponse(BaseModel):
    files: List[FileResponse]

class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str = "success"

# ------------------------------
# Email Verification
# ------------------------------

class EmailVerificationResponse(BaseModel):
    message: str
