from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from passlib.context import CryptContext

SECRET_KEY = "$2a$12$xU/BB.GtVG2SOn3WgT2xruCZ8htpyHFXoIrmTeMfnT2EZ0JP2zrkS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(myToken: str):
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException("Invalid token: missing subject")
    except JWTError:
        raise CredentialsException("Invalid token: JWT decoding failed")
    return username

class CredentialsException(Exception):
    def __init__(self, message="Could not validate credentials"):
        self.message = message
        super().__init__(self.message)