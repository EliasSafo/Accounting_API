from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int) -> schemas.User:  # return types
    try:
        db_user = db.query(models.User).get(user_id)
    except LookupError:
        print("User not found")
    return db_user


def get_all_users(db: Session) -> list[schemas.User]:
    try:
        db_users = db.query(models.User).all()
    except LookupError:
        print("User not found")
    return db_users


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, balance=user.balance, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    db.refresh()
    return db_user


def update_user_balance(db: Session, user_id: int, balance: float):
    db_user = get_user(db, user_id)
    db_user.balance = balance
    db.commit()
