from fastapi import FastAPI, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from database import engine, LocalSession, Base
from models import Users
from auth_utils import hashed_password, password_verification, createToken, decode_access_token
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



app = FastAPI()
security = HTTPBearer()
Base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


class CreateUser(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: CreateUser, db: Session = Depends(get_db)):
    exist = db.query(Users).filter(Users.username == user.username).first()
    if exist:
        raise HTTPException(status_code=400,detail="user already exists")
    hash_password = hashed_password(user.password)
    new_user = Users(username=user.username, hashedPassword=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # db.close()
    return {"username":new_user.username, "id": new_user.id}

@app.post("/login")
def login(user: CreateUser, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if not db_user or not password_verification(user.password, db_user.hashedPassword):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    acces_token = createToken(data={"sub":db_user.username})
    return {
        "access_token": acces_token,
        "token_type": "bearer",
        "user": db_user
    }
