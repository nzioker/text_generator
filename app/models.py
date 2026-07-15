import email
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    names = Column(String(100), index=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    generations = relationship("Generations", back_populates="user")


class Generations(Base):
    __tablename__ = "generation"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    prompt = Column(String, index=True)
    response = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="generations")
