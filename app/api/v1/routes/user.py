from fastapi import APIRouter, Depends, HTTPException, status
from app.services import user_services
from app.schemas.user import UserCreate, ShowUser
from app.core.database import get_db
from sqlalchemy.orm import Session


user_route = APIRouter(prefix="/users", tags=["Users"])


# create a user
@user_route.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_services.get_user_by_email(request.email, db)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_services.create_user(request, db)



# get all users
@user_route.get( "/", response_model=list[ShowUser], status_code=status.HTTP_200_OK)
async def read_all_users(db : Session = Depends(get_db)):
    return user_services.get_all_users(db)


# get a user by id
@user_route.get("/{user_id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_services.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


# get user by email
@user_route.get("/email/{email}", response_model=ShowUser, status_code=status.HTTP_200_OK)
async def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = user_services.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    return user


# get user by username
@user_route.get("/username/{username}", response_model=ShowUser, status_code=status.HTTP_200_OK)
async def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = user_services.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    return user


# update a user
@user_route.put("/{user_id}", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def update_user(user_id: int, request: UserCreate, db: Session = Depends(get_db)):
    user = user_services.update_user(user_id, request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


# delete a user
@user_route.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = user_services.delete_user(user_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return {"message": "User deleted successfully"}
