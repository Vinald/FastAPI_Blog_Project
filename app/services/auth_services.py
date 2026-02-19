from app.models.user import User
from app.core.security import verify_password, create_access_token
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.config import settings


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    """Authenticate user by email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def login_user(email: str, password: str, db: Session) -> dict:
    """Login user and return access token"""
    user = authenticate_user(email, password, db)
    if not user:
        return {"success": False, "message": "Invalid email or password"}

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id
    }
