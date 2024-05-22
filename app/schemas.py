from pydantic import BaseModel
from typing import List, Optional

# Token schema ------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

# Car schema --------------------------------------
class CarBase(BaseModel):
    carName: str
    carYear: int
    carColor: str
    carPrice: float
    image_url: str
    carDescription: Optional[str] = None

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# User schema -------------------------------------
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    cars: List[Car] = []

    class Config:
        from_attributes = True
