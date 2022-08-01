from sqlalchemy import Column, ForeignKey, String, REAL, Integer
from . database import BASE


class UserModel(BASE):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(Integer)
    email = Column(String)
    password = Column(String)

    class Meta:
        load_instance = True


class TransactionModel(BASE):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    Amount = Column(REAL)
    MpesaReceiptNumber = Column(String)
    TransactionDate = Column(String)
    PhoneNumber = Column(Integer)

    class Meta:
        load_instance = True
