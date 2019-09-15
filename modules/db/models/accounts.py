
from sqlalchemy import Table, Column,UniqueConstraint, Sequence, ForeignKey
from sqlalchemy import BigInteger, Integer, String, DateTime, Float, Enum , Boolean, Text
from .base import Base

import bcrypt

class Account(Base):
    __tablename__ = 'accounts'

    id = Column('id', Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)

    user_id = Column('user_id', String(32), unique=True , nullable=False)
    display_name = Column('display_name', String(32), nullable=False)
    password = Column('password', String(64), nullable=False)
    

    def __init__(self, user_id, display_name, password):
        self.user_id = user_id
        self.display_name = display_name

        # using salt
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode(), salt)

    def check_password(self, given_password):
        return bcrypt.checkpw(given_password.encode(), self.password.encode())
        

