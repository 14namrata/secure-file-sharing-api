from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from passlib.hash import bcrypt
from passlib.context import CryptContext
import os

from app.utils.auth import get_current_client_user
from app.utils.database import get_db
from app.utils.mailer import send_verification_email
from app.utils.token import generate_token, verify_token, create_access_token
from app.models import FileUpload, Client
from app.schemas import LoginData
from app.schemas import LoginData, SignupData, DownloadLinkResponse, EmailVerificationResponse

router = APIRouter(tags=["Client"])  # Removed prefix here


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
def signup(username: str, password: str, email: str, db: Session = Depends(get_db)):
    """
    Signup a new client and send verification email.
    """
    if db.query(Client).filter(Client.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = bcrypt.hash(password)
    user = Client(
        username=username,
        hashed_password=hashed_pw,
        email=email,
        role="client",
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = generate_token(email)
    send_verification_email(email, token)

    return {
        "message": "User registered successfully. Check email for verification.",
        "verify_link": f"http://127.0.0.1:8000/client/verify-email?token={token}"
    }


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify client's email using the token.
    """
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    client = db.query(Client).filter(Client.email == email).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/login")
def client_login(login_data: LoginData, db: Session = Depends(get_db)):
    """
    Client login endpoint
    """
    user = db.query(Client).filter(Client.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not pwd_context.verify(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": "client"},
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }


@router.get("/download/{file_id}", response_class=FileResponse)
def download_file(
    file_id: int,
    current_user=Depends(get_current_client_user),
    db: Session = Depends(get_db)
):
    """
    Download file for client user by file ID.
    Requires client authentication.
    """
    file = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found in database.")

    file_path = os.path.join("uploads", file.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk.")

    return FileResponse(
        path=file_path,
        filename=file.filename,
        media_type="application/octet-stream"
    )
