from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from app.services.auth_service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    tokens = AuthService.register(db, data)
    return TokenResponse(**tokens)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    tokens = AuthService.login(db, data)
    return TokenResponse(**tokens)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest):
    access = AuthService.refresh_token(data.refresh_token)
    return TokenResponse(access_token=access["access_token"], refresh_token=data.refresh_token)
