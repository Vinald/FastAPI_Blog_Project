from fastapi import APIRouter, Depends
from app.schemas.auth import  LoginRequest
from app.core.database import get_db
from sqlalchemy.orm import Session


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
    summary="User login",
    description="Authenticate a user and return an access token.",
    response_description="Access token for authenticated user"
)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user with their email and password. If the credentials are valid, an access token will be returned.
    """
    return {"message": "Login endpoint - to be implemented"}
