"""importing"""
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    """password hashing function"""
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    """password verify function"""
    return pwd_context.verify(plain_password, hashed_password)