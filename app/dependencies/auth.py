from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.exceptions.auth import (
    InvalidCredentialsException,
    UserNotFoundException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    try:
        payload = decode_access_token(token)

        email = payload.get("sub")

        if email is None:
            raise InvalidCredentialsException()

    except Exception:
        raise InvalidCredentialsException()

    user = UserRepository.get_by_email(
        db,
        email,
    )

    if user is None:
        raise UserNotFoundException()

    if not user.is_active:
        raise InvalidCredentialsException()

    return user