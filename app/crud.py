
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas, token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(db: Session, myToken: str):
    username = token.verify_token(myToken)
    user = get_user_by_username(db, username)
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, username: int, myToken: str):
    usernameToken = token.verify_token(myToken)
    if usernameToken == username:
        return get_user_by_username(db, username)

def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    password_hashed = pwd_context.hash(user.password)
    db_user = models.User(**user.model_dump(), hashed_password=password_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Car).offset(skip*limit).limit(limit).all()

def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()

def create_user_car(db: Session, car: schemas.CarCreate, token: str):
    current_user = get_current_user(db, token)
    db_car = models.Car(**car.dict(), owner_id=current_user.id)

    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    return db_car

def edit_user_car(db: Session, car_id: str, car: schemas.CarCreate, token: str):
    current_user = get_current_user(db, token)
    current_car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == current_user.id).first()
    if not current_user:
        return None
    for key, value in car.dict(exclude_unset=True).items():
        setattr(current_car, key, value)

    db.commit()
    db.refresh(current_car)

    return current_car