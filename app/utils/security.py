# app/utils/security.py
import bcrypt

def password_hash(password: str) -> str:
    """Converts a plain-text password into a secure, undecryptable hash string."""
    # 1. Convert the plain text password string into bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generate a random cryptographic 'salt'
    salt = bcrypt.gensalt()
    
    # 3. Hash the bytes using the salt
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Convert the final byte string back to a normal text string for our database column
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain text input with the stored hash to see if they match."""
    # Convert both fields back to bytes for bcrypt's comparison calculation
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Safely checks if the plain input matches the cryptographic footprint of the hash
    return bcrypt.checkpw(plain_bytes, hashed_bytes)
