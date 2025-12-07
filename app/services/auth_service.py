from fastapi import HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings
from app.repositories.user_repo import UserRepository

pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthService:

    @staticmethod
    def register(db, data):
        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        if data.password != data.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        hashed = pwd.hash(data.password)
        user = UserRepository.create(db, data.email, hashed, data.full_name)

        return {
            "access_token": create_access_token({"sub": str(user.id)}),
            "refresh_token": create_refresh_token({"sub": str(user.id)}),
        }

    @staticmethod
    def login(db, data):
        user = UserRepository.get_by_email(db, data.email)
        if not user or not pwd.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": create_access_token({"sub": str(user.id)}),
            "refresh_token": create_refresh_token({"sub": str(user.id)}),
        }

    @staticmethod
    def refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        return {
            "access_token": create_access_token({"sub": str(user_id)}),
        }

    @staticmethod
    def get_current_user(db, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
