from fastapi import FastAPI, status, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from utils.schemas import Transaction, User
from utils.database import SessionLocal, engine
from utils.models import UserModel, TransactionModel
import crud
from utils.models import BASE

BASE.metadata.create_all(bind=engine)

app = FastAPI()
load_dotenv()

mpesa_key = os.getenv('MPESA-KEY')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.get('/{key}', status_code=status.HTTP_200_OK)
def home(key: str):
    if not key:
        return "key is required"
    if key != mpesa_key:
        return {"Status": "Invalid Key."}
    return {'Code': status.HTTP_200_OK, 'Status': 'Server is Up and Running...'}


@app.post('/api/tbuy/users/', status_code=status.HTTP_201_CREATED)
async def add_user(user: User, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db=db, user=user)
    except:
        return "Error creating user"


@app.get('/api/tbuy/users/{key}', status_code=status.HTTP_200_OK)
async def get_all_users(key: str, db: Session = Depends(get_db)):
    mpesa_key = 'key.mpesakenya'
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Key is required.")
    if key != mpesa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Key!")
    try:
        return crud.get_all_users(db=db)
    except:
        return "Errorr Fetching users from database"


@app.get('/api/tbuy/users/sortby-id/{user_id}/{key}', status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, key: str, db: Session = Depends(get_db)):
    try:
        if not key:
            return {"Result": "key required!"}
        if key != mpesa_key:
            return {"Key Error": "Invalid Key"}
        user = crud.get_user_by_id(db=db, user_id=user_id)
        if not user:
            return f"User with id {user_id} not Found."
        return user
    except:
        return "Error fetching user by id"


@app.get('/api/tbuy/users/sortby-mobile-number/{mobile_number}/{key}', status_code=status.HTTP_200_OK)
async def get_user_by_phone_number(mobile_number: int, key: str, db: Session = Depends(get_db)):
    if not mobile_number:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Mobile number is required")
    try:
        return crud.get_user_by_phone(db=db, phone=mobile_number)
    except:
        return "Error fetching user by phone number"


@app.delete('/api/tbuy/users/delete/{key}/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(key: str, phone_number: int, db: Session = Depends(get_db)):
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Key is required.")
    if key != mpesa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Key.")
    user = db.query(UserModel).filter(UserModel.phone_number == phone_number)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    user.delete(synchronize_session=False)
    db.commit()
    return "User Deleted"


# ************************* TRANSACTIONS ******************************
# *********************************************************************
@app.post('/api/tpay/transactions/{key}', status_code=status.HTTP_201_CREATED)
async def add_transaction(transaction: Request, key: str, db: Session = Depends(get_db)):
    trans_data = await transaction.json()
    trans_dict = {}
    code = trans_data['Body']['stkCallback']
    if key != mpesa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Access Key!!')
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access Key is Missing!!')
    if code['ResultCode'] > 0:
        return {"Results": "Transaction Failed!"}
    else:
        try:
            trans = code['CallbackMetadata']["Item"]
            del(trans[2])
            for k in trans:
                trans_dict[k['Name']] = k['Value']
            return crud.create_transaction(db=db, trans=trans_dict)
        except:
            return {"Error": "Something went wrong."}


@app.get('/api/tpay/transactions/{key}', status_code=status.HTTP_200_OK)
async def get_transactions(key: str, db: Session = Depends(get_db)):
    return crud.get_all_transactions(db=db)


@app.get("/api/tpay/transactions/sortby-mobile-number/{mobile_number}/{key}")
async def get_transaction_by_mobile_number(key: str, number: int, db: Session = Depends(get_db)):
    return crud.get_transaction_by_mobile_number(db=db, number=number)


@app.delete('/api/tpay/transactions/delete-by-receipt/{receipt_number}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_by_receipt(receipt_number: str, db: Session = Depends(get_db)):
    transaction = db.query(TransactionModel).filter(
        TransactionModel.MpesaReceiptNumber == receipt_number)
    if not transaction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction not found.")
    transaction.delete(synchronize_session=False)
    db.commit()
    return "transaction Deleted"


@app.delete('/api/tpay/transactions/delete-by-pnone/{key}/{mobile}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_by_receipt(key: str, mobile: int, db: Session = Depends(get_db)):
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Key is required")
    if key != mpesa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Key.")
    transaction = db.query(TransactionModel).filter(
        TransactionModel.PhoneNumber == mobile)
    if not transaction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction not found.")
    transaction.delete(synchronize_session=False)
    db.commit()
    return "transaction Deleted"
