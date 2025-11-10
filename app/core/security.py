import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Optional, Callable

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.users import User


SECRET_KEY = os.getenv("AUTH_SECRET", "dev-secret-change-me")
TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TTL", "86400"))  # 24h


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode())


def hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or base64.urlsafe_b64encode(os.urandom(12)).decode()
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"sha256${salt}${h}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        algo, salt, digest = hashed.split("$", 2)
        if algo != "sha256":
            return False
    except ValueError:
        return False
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return h == digest


def create_token(*, sub: str, role: str, rut: Optional[str]) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {"sub": sub, "role": role, "rut": rut, "iat": now, "exp": now + TOKEN_TTL_SECONDS}
    header_b64 = _b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    sig = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    token = f"{header_b64}.{payload_b64}.{_b64url(sig)}"
    return token


@dataclass
class AuthUser:
    username: str
    role: str
    rut: Optional[str]


def decode_token(token: str) -> AuthUser:
    try:
        header_b64, payload_b64, signature = token.split(".", 3)
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, _b64url_decode(signature)):
            raise ValueError("Firma inválida")
        payload = json.loads(_b64url_decode(payload_b64))
        if int(time.time()) >= int(payload.get("exp", 0)):
            raise ValueError("Token expirado")
        return AuthUser(username=payload.get("sub"), role=payload.get("role"), rut=payload.get("rut"))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")


_bearer = HTTPBearer(auto_error=True)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> AuthUser:
    token = credentials.credentials
    return decode_token(token)


def require_role(*roles: str) -> Callable[[AuthUser], AuthUser]:
    def _dep(user: AuthUser = Depends(get_current_user)) -> AuthUser:
        if roles and user.role not in roles:
            raise HTTPException(403, detail="Permisos insuficientes")
        return user
    return _dep


def ensure_default_users(db: Session):
    # Crea un admin y un trabajador por defecto si no existen
    defaults = [
        {
            "username": "admin",
            "full_name": "Administrador",
            "rut": None,
            "role": "admin",
            "password": "admin123",
        },
        {
            "username": "chofer",
            "full_name": "Trabajador",
            "rut": "21421299-4",
            "role": "worker",
            "password": "chofer123",
        },
    ]
    for u in defaults:
        existing = db.query(User).filter(User.username == u["username"]).first()
        if not existing:
            db.add(
                User(
                    username=u["username"],
                    full_name=u["full_name"],
                    rut=u["rut"],
                    role=u["role"],
                    hashed_password=hash_password(u["password"]),
                    is_active=1,
                )
            )
    db.commit()

