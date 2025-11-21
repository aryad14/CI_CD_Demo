from pydantic import BaseModel, EmailStr
from datetime import datetime

# ----------- Request Schemas -----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None


# ----------- Response Schemas -----------

class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True   # SQLAlchemy → Pydantic conversion
