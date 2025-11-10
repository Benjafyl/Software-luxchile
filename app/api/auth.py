from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.users import User
from app.core.security import create_token, verify_password, ensure_default_users, get_current_user, AuthUser


router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    ensure_default_users(db)
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail="Credenciales inválidas")
    token = create_token(sub=user.username, role=user.role, rut=user.rut)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "rut": user.rut,
        },
    }


@router.get("/me")
def me(current: AuthUser = Depends(get_current_user)):
    return current.__dict__

