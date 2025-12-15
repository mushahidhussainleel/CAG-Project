# src/utils/password_utils.py
from passlib.context import CryptContext

# Create a CryptContext for hashing and verifying passwords
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt.
    bcrypt automatically generates a secure salt.
    """
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifies a plain password against its hashed password.
    """
    return pwd_context.verify(password, password_hash)
