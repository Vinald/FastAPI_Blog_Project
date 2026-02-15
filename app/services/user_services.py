from app.models.user import User
from app.schemas.user import UserCreate, ShowUser
from sqlalchemy.orm import Session


def create_user(user_data: UserCreate, db: Session):
    new_user = User(name=user_data.name, email=user_data.email, password=user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.name == username).first()


def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()


def update_user(user_id: int, user_data: UserCreate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = user_data.name
        user.email = user_data.email
        user.password = user_data.password
        db.commit()
        db.refresh(user)
        return user
    return None


def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
