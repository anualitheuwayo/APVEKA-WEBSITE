# app/routers/auth_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut, Token, LoginRequest
from app.core import get_current_user, require_headmaster
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_headmaster),
):
    return auth_service.register_user(db, payload)


@router.post("/bootstrap-headmaster", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def bootstrap_first_headmaster(payload: UserCreate, db: Session = Depends(get_db)):
    return auth_service.bootstrap_first_headmaster(db, payload)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login(db, payload.username, payload.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user