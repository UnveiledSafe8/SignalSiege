from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timezone, timedelta

import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def get_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(plaintext: str, hashed):
    return pwd_context.verify(plaintext, hashed)

def create_access_token(data: dict):
    data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    data["expire"] = expire.timestamp()
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)