from app.models import User, SessionLocal
from app.utils.encryption import hash_password

db = SessionLocal()
existing_user = db.query(User).filter(User.email == "newuser@example.com").first()

if existing_user:
    print("User already exists.")
else:
    user = User(
        email="newuser@example.com",
        password=hash_password("yourStrongPassword123"),
        role="ops"
    )
    db.add(user)
    db.commit()
    print("User inserted successfully.")
