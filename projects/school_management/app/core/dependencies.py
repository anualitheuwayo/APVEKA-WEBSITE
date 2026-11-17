from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from database import get_db
from app.models import User, RoleEnum
from app.core.security import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Runs on every protected endpoint. Reads the token from the
    'Authorization: Bearer <token>' header, decodes it, and looks up
    the matching user in the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_headmaster(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != RoleEnum.headmaster:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the headmaster can perform this action",
        )
    return current_user