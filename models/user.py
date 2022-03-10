from .base import Base
from sqlalchemy import Column, String, Integer

class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String,nullable=False)
    password = Column(String,nullable=False)

    def __init__(self,username, password):
        self.username = username
        self.password = password