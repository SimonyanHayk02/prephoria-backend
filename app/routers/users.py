from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse, UpdateUser
from app.services.auth_service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/me", response_model=UserResponse)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = AuthService.get_current_user(db, token)
    return user

@router.put("/me", response_model=UserResponse)
def update_me(
    update: UpdateUser,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = AuthService.get_current_user(db, token)
    updated = AuthService.update_user(db, user, update)
    return updated
