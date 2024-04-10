from fastapi import FastAPI, Depends, HTTPException

import models
import schemas
import crud
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root_get() -> str:
    return "Hello World"


@app.get("/users/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@app.post("/users/", response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/user/{id}", response_model=schemas.User)
async def get_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)


@app.put("/transaction", response_model=dict[str, float])
async def transfer_money(
    sender_id: int, reciever_id: int, amount: float, db: Session = Depends(get_db)
):
    sender = crud.get_user(db=db, user_id=sender_id)
    receiver = crud.get_user(db=db, user_id=reciever_id)
    if sender.balance < amount:
        raise HTTPException(
            status_code=400, detail="Insufficient funds in sender's account"
        )
    sender.balance -= amount
    receiver.balance += amount
    db.commit()
    return {"sender": sender.balance, "receiver": receiver.balance}


@app.put("/withdraw",response_model=schemas.User)
async def withdraw_money(user_id:int, amount:float, db:Session=Depends(get_db)):
    if amount < 0 :
        raise HTTPException(
            status_code=403, detail="You cannot withdraw negative funds"
        )
    user = crud.get_user(db=db, user_id=user_id)
    user.balance-= amount
    db.commit()
    return user

@app.put("/deposit",response_model=schemas.User)
async def deposit_money(user_id:int, amount:float, db:Session=Depends(get_db)):
    if amount < 0 :
        raise HTTPException(
            status_code=403, detail="You cannot deposit negative funds"
        )
    user = crud.get_user(db=db, user_id=user_id)
    user.balance+= amount
    db.commit()
    return user


