from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class ShowUser(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# For nested blog display (without circular reference)
class BlogInUser(BaseModel):
    id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class ShowUserWithBlogs(UserBase):
    id: int
    blogs: list[BlogInUser] = []

    model_config = ConfigDict(from_attributes=True)
