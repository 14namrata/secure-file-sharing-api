from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from jose import jwt

# Email token config
SECRET_KEY = "your-very-secret-key"  # Ideally from os.getenv in production
SECURITY_SALT = "email-confirm-salt"

# JWT config
JWT_SECRET_KEY = "your-jwt-secret-key"  # Also replace with environment variable in prod
ALGORITHM = "HS256"


# -- EMAIL VERIFICATION TOKEN FUNCTIONS --

def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_SALT)

def verify_token(token: str, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        return serializer.loads(token, salt=SECURITY_SALT, max_age=expiration)
    except Exception:
        return None


# -- JWT ACCESS TOKEN FUNCTION --

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
