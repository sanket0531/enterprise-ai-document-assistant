from sqlalchemy.orm import Session

from app.exceptions.auth import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserLogin
from app.utils.jwt import create_access_token
from app.utils.security import verify_password


class AuthService:

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin,
    ) -> Token:

        user = UserRepository.get_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        if not user.is_active:
            raise InactiveUserException()

        access_token = create_access_token(
            data={
                "sub": user.email,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )