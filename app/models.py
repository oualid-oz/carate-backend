from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, index=True)
    hashed_password = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    cars = relationship("Car", back_populates="owner")

    def __init__(self, username: str, full_name: str, email: str, hashed_password: str, password: str, is_active: bool = True):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.hashed_password = hashed_password
        self.password = password
        self.is_active = is_active
  
class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    carName = Column(String, index=True)
    carYear = Column(Integer)
    carColor = Column(String)
    carDescription = Column(String)
    carPrice = Column(Float)
    image_url= Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="cars")
