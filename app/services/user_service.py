from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from app.exceptions.auth import UserAlreadyExistsException

class UserService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise UserAlreadyExistsException(user_data.email)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
            role=UserRole.VIEWER,
        )

        return UserRepository.create(
            db,
            user,
        )