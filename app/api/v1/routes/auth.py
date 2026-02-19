from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.auth_services import login_user


auth_route = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)


@auth_route.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate a user and return a JWT access token.",
    response_description="JWT access token for authenticated user"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user with their email and password.

    - **username**: User's email address
    - **password**: User's password

    Returns a JWT access token if credentials are valid.
    """
    result = login_user(form_data.username, form_data.password, db)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("message", "Invalid credentials"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=result["access_token"], token_type=result["token_type"])
