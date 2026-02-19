from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
