from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

# File endpoints
@app.post("/files/", response_model=schemas.File)
def upload_file(file: schemas.FileCreate, db: Session = Depends(get_db)):
    return crud.create_file(db, file)

@app.get("/files/", response_model=list[schemas.File])
def read_files(db: Session = Depends(get_db)):
    return crud.get_files(db)

