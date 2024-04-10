from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    balance: float
    role: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
