from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str


class ShowUser(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserPost(UserBase):
    password: str
