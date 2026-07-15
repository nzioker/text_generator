from app.models import Base, User, Generations
from app.database.database import engine

def create_tables():
    Base.metadata.create_all(bind=engine)


