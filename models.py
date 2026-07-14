import email
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    names = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)
    generations = relationship("Generations", back_populates="user")


class Generations(Base):
    __tablename__ = "generation"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    prompt = Column(String, index=True)
    response = Column(String, index=True)
    created_at = Column(index=True)
    user = relationship("User", back_populates="gen_id")
