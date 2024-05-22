from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, models, schemas, token
from app.database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/login", response_model=schemas.Token, tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(days=token.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/signup", response_model=schemas.User, tags=["Auth"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    username_exist = crud.get_user_by_username(db=db , username = user.username)
    if username_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")
    
@app.get("/api/logout", tags=["Auth"])
def logout(token: str = Depends(oauth2_scheme)):
    return {"message": "Logout successful"}

@app.post("/api/cars/", response_model=schemas.Car, tags=["Cars"])
def create_car_for_user(car: schemas.CarCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    my_car = crud.create_user_car(db=db, car=car, token=token)
    if my_car is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not authenticated")
    return my_car

@app.get("/api/cars/", response_model=List[schemas.Car], tags=["Cars"])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    cars = crud.get_cars(db, skip=skip, limit=limit)
    if cars is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cars not found")
    return cars

@app.get("/api/cars/user/{username}", response_model=List[schemas.Car], tags=["Cars"])
def read_cars_by_user(username: str = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = crud.get_user(db, username=username, myToken=token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You don't have any cars yet")
    return user.cars

@app.get("/api/cars/car/{car_id}", response_model=schemas.Car, tags=["Cars"])
def read_car(car_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    car = crud.get_car(db, car_id=car_id, myToken=token)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car
