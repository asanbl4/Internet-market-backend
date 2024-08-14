from database import Base
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)