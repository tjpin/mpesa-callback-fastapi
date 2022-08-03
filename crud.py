from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from utils import models, schemas

# *************************** USERS **************************************
# ************************************************************************


def create_user(db: Session, user: schemas.User):
    new_user = models.UserModel(**user.dict())
    user_indb = db.query(models.UserModel).filter(
        models.UserModel.phone_number == new_user.phone_number).first()
    if user_indb:
        raise HTTPException(detail="User already registered.",
                            status_code=status.HTTP_409_CONFLICT)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session, skip: int = 0):
    return db.query(models.UserModel).offset(skip).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_phone(db: Session, phone: int):
    return db.query(models.UserModel).filter(models.UserModel.phone_number == phone).first()


# *************************** Transactions **************************************
# *******************************************************************************
def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(models.TransactionModel).filter(models.TransactionModel.id == transaction_id).first()


def get_transaction_by_mobile_number(db: Session, number: int):
    return db.query(models.TransactionModel).filter(models.TransactionModel.PhoneNumber == number).first()


def get_all_transactions(db: Session, skip: int = 0):
    return db.query(models.TransactionModel).offset(skip).all()


def create_transaction(db: Session, trans: schemas.Transaction):
    db_trans = models.TransactionModel(**trans)
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans
