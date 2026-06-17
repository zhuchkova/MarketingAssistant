import os
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24 * 7  # 7 days

_bearer = HTTPBearer()


def get_secret_key() -> str:
    if not SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is required")
    return SECRET_KEY


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_token(user_id: str, email: str, name: str = "") -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, get_secret_key(), algorithms=[ALGORITHM])
        return {"user_id": payload["sub"], "email": payload["email"], "name": payload.get("name", "")}
    except RuntimeError:
        raise HTTPException(status_code=500, detail="Authentication is not configured")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
