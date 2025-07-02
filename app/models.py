from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class FileUpload(Base):
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)  # ✅ Added length for MySQL


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)       # ✅ length added
    hashed_password = Column(String(255), nullable=False)             # ✅ length added
    role = Column(String(50), nullable=False)                         # ✅ length added
    is_verified = Column(Boolean, default=False)
