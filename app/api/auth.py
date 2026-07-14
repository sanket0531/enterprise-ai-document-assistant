from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return UserService.register_user(
        db,
        user_data,
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    credentials = UserLogin(
        email=form_data.username,   # OAuth2 uses "username" field
        password=form_data.password,
    )

    return AuthService.login(
        db=db,
        credentials=credentials,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user