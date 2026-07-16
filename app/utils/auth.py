# app/utils/auth.py
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

# Secret keys are used to digitally sign the token so users cannot forge or edit them
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    """Generates a secure, signed JWT token string that expires after a set window."""
    # 1. Create a copy of the incoming data payload (e.g., {"user_id": 5})
    to_encode = data.copy()
    
    # 2. Calculate the exact expiration timestamp using a fixed UTC reference
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 3. Add the 'exp' claim to the token payload (JWT standard lookup key for expiration checks)
    to_encode.update({"exp": expire})
    
    # 4. Sign and compile the token into a neat text string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# This tells FastAPI to look for an "Authorization: Bearer <TOKEN>" entry in the request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Intercepts incoming requests, decodes the token, and extracts the valid user ID."""
    try:
        # Decode the token payload using our fixed secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Pull out the user_id integer we packed into the token during the /login step
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing identification."
            )
        
        # Access verified! Pass the user_id down to our route function
        return user_id
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or manipulated access token validation failed."
        )

