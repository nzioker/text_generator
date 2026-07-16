import email
import json
from socket import timeout
from fastapi import FastAPI, HTTPException, Depends, status
from contextlib import asynccontextmanager
from app.utils.db_init import create_tables
import httpx
import os
from app.models import Generations, User
from app.database.database import get_db, sessionLocal
from sqlalchemy.orm import Session
import redis
from app.utils.dependencies import rate_limiter
from app.utils.security import password_hash, verify_password
from app.utils.auth import create_access_token
from app.utils.auth import get_current_user_id
from dotenv import load_dotenv

from schemas import GenerationRequest, UserCreate

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    # Create User
    db = sessionLocal()
    try:
        # Check if our test user with ID 1 already exists
        test_user = db.query(User).filter(User.id == 1).first()
        if not test_user:
            # Create a mock default user
            new_user = User(id=1, names="test_developer")
            db.add(new_user)
            db.commit()
            print("👤 Seeded default test user (ID: 1) into the database.")
    except Exception as e:
        print(f"Warning during seeding: {e}")
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.email == payload.email)  | (User.names == payload.names)).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    hashed_pwd = password_hash(payload.password)

    new_user = User(names=payload.names, email=payload.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id":new_user.id,
        "Username":new_user.names,
        "Email":new_user.email,
        "Message": "User registered succesfully."
    }

@app.post("/login")
def login(payload:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if not existing_user:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    password_match = verify_password(payload.password, existing_user.password)
    if not password_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token_payload = {"user_id":existing_user.id, "username": existing_user.names}
    access_token = create_access_token(data=token_payload)

    return {
        "access_token": access_token,
        "token_type": "bearer_token",
        "message": "Login succesfull"
    }
    

@app.get("/health")
def health_check():
    return {"Status": "Running"}


@app.get("/")
def home():
    return "This is home."


@app.post("/generate", dependencies=[Depends(rate_limiter)])
async def generate(payload: GenerationRequest, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):

    llama_url = "http://ai:11434/api/generate"
    data = {
        "model":"phi3",
        "prompt":payload.prompt,
        "stream":False
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(llama_url, json=data, timeout=None)
            response.raise_for_status()

            result = response.json()
            ai_generated_text = result.get("response")

            new_instance = Generations(
                prompt = payload.prompt,
                response = ai_generated_text,
                user_id = current_user_id
            )

            db.add(new_instance)
            db.commit()
            db.refresh(new_instance)

            return {
                "id":new_instance.id,
                "prompt":new_instance.prompt,
                "response":new_instance.response,
                "created_at":new_instance.created_at
            }
            
        except httpx.HTTPError as err:
            raise HTTPException(status_code=500, detail=f"Failed to communicate with the AI service{err}")
        
    return "Generate text"


@app.get("/history")
def history(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    cache_key = f"user:{current_user_id}:history"

    cached_history = redis_client.get(cache_key)

    if cached_history:
        return json.loads(cached_history)
    
    history_records = db.query(Generations).filter(Generations.user_id == current_user_id).all()

    history_list = []
    
    for record in history_records:
        history_list.append({"id":record.id, 
      "prompt":record.prompt, 
      "response":record.response, 
      "created_at":record.created_at.isoformat() if record.created_at else None
      })
    
    redis_client.setex(
        name=cache_key,
        time=300,
        value=json.dumps(history_list)
    )

    

    return history_list
