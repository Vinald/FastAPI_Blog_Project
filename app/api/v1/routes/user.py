from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.services import user_services
from app.schemas.user import UserCreate, ShowUser, ShowUserWithBlogs
from app.core.database import get_db
from sqlalchemy.orm import Session


user_route = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    }
)


# create a user
@user_route.post(
    "/",
    response_model=ShowUser,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with name, email, and password. The password will be hashed before storing.",
    response_description="The created user"
)
async def create_user(
    request: UserCreate = Body(
        ...,
        examples=[
            {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123"
            }
        ]
    ),
    db: Session = Depends(get_db)
):
    """
    Create a new user with the following information:

    - **name**: User's full name
    - **email**: User's email address (must be unique)
    - **password**: User's password (will be hashed)
    """
    existing_user = user_services.get_user_by_email(request.email, db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_services.create_user(request, db)



# get all users
@user_route.get(
    "/",
    response_model=list[ShowUser],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    description="Retrieve a list of all registered users."
)
async def read_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.
    """
    return user_services.get_all_users(db)


# get a user by id (with blogs)
@user_route.get(
    "/{user_id}",
    response_model=ShowUserWithBlogs,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID, including their blogs."
)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID with all their associated blogs.

    - **user_id**: The unique identifier of the user
    """
    user = user_services.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


# get user by email
@user_route.get(
    "/email/{email}",
    response_model=ShowUser,
    status_code=status.HTTP_200_OK,
    summary="Get user by email",
    description="Retrieve a specific user by their email address."
)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get a user by their email address.

    - **email**: The email address of the user
    """
    user = user_services.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    return user


# get user by username
@user_route.get(
    "/username/{username}",
    response_model=ShowUser,
    status_code=status.HTTP_200_OK,
    summary="Get user by username",
    description="Retrieve a specific user by their username."
)
async def read_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a user by their username.

    - **username**: The username of the user
    """
    user = user_services.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    return user


# update a user
@user_route.put(
    "/{user_id}",
    response_model=ShowUser,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    description="Update an existing user's information."
)
async def update_user(
    user_id: int,
    request: UserCreate = Body(
        ...,
        examples=[
            {
                "name": "John Updated",
                "email": "john.updated@example.com",
                "password": "newpassword123"
            }
        ]
    ),
    db: Session = Depends(get_db)
):
    """
    Update a user's information.

    - **user_id**: The unique identifier of the user to update
    - **name**: New name for the user
    - **email**: New email for the user
    - **password**: New password (will be hashed)
    """
    user = user_services.update_user(user_id, request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


# delete a user
@user_route.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    description="Delete a user from the database.",
    responses={
        200: {
            "description": "User deleted successfully",
            "content": {
                "application/json": {
                    "example": {"message": "User deleted successfully"}
                }
            }
        }
    }
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    - **user_id**: The unique identifier of the user to delete
    """
    deleted = user_services.delete_user(user_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return {"message": "User deleted successfully"}
