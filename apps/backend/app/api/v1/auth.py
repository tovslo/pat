from datetime import timedelta

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from jose import JWTError
from pydantic import EmailStr, TypeAdapter
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.deps import get_current_user, get_db
from app.core.security import (
    create_access_token,
    create_email_token,
    decode_email_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    UserResponse,
    VerifyEmailRequest,
)
from app.services.s3 import upload_avatar
from app.tasks.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])

_COOKIE_NAME = "access_token"
_COOKIE_OPTS = {
    "httponly": True,
    "samesite": "lax",
    "secure": False,  # True in production (HTTPS)
    "max_age": settings.jwt_expire_minutes * 60,
}

_email_adapter = TypeAdapter(EmailStr)


def _verification_url(token: str) -> str:
    base = settings.frontend_url.rstrip("/")
    return f"{base}/auth/verify-email?token={token}"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    email: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        _email_adapter.validate_python(email)
    except PydanticValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Введите корректный email"
        ) from None

    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Пароль должен содержать минимум 8 символов",
        )

    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email уже зарегистрирован"
        )

    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    await db.flush()  # get user.id before committing

    if avatar and avatar.content_type:
        data = await avatar.read()
        try:
            avatar_url = await upload_avatar(data, avatar.content_type, user.id)
            user.avatar_url = avatar_url
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    await db.commit()

    token = create_email_token(email)
    url = _verification_url(token)
    send_verification_email.delay(email, url)

    return {"detail": "Письмо с подтверждением отправлено"}


@router.post("/login")
async def login(
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email не подтверждён. Проверьте почту.",
        )

    token = create_access_token(user.id, timedelta(minutes=settings.jwt_expire_minutes))
    response.set_cookie(_COOKIE_NAME, token, **_COOKIE_OPTS)
    return UserResponse.from_orm_user(user)


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(_COOKIE_NAME)
    return {"detail": "Выход выполнен"}


@router.post("/verify-email")
async def verify_email(
    body: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    try:
        email = decode_email_token(body.token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недействительная или устаревшая ссылка"
        ) from None

    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    if not user.is_verified:
        user.is_verified = True
        await db.commit()

    return {"detail": "Email подтверждён"}


@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.from_orm_user(current_user)


@router.post("/avatar")
async def update_avatar(
    avatar: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    data = await avatar.read()
    try:
        avatar_url = await upload_avatar(data, avatar.content_type or "", current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    current_user.avatar_url = avatar_url
    await db.commit()
    await db.refresh(current_user)
    return UserResponse.from_orm_user(current_user)
