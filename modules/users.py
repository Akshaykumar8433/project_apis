from sqlalchemy import Column,BigInteger,String, DateTime
from sqlalchemy.sql.expression import column
from dbconnect import Base
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Users(Base):
    __tablename__ = "users"
    email: str
    password: str
    id: int
    role: str

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    email = Column(String(255),unique=True)
    password = Column(String(255))
    role = Column(String(10))

    def __init__(self,email="",password="",role="user"):
        self.email = email
        self.password = password
        self.role = role

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    def get_role(self):
        return self.role

    def get_id(self):
        return self.id