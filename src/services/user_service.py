# src/services/user_service.py
from src.database.memory_db import users, next_user_id
from src.utils.password_utils import hash_password, verify_password

# -------------------------------
# Create a new user
# -------------------------------
def create_user(name: str, email: str, country: str, password: str, purpose: str = None) -> dict:
    """
    Creates a new user and stores in the in-memory database.
    Raises ValueError if the email already exists.
    """
    global next_user_id
    if email in users:
        raise ValueError("User already exists")
    
    user = {
        "user_id": next_user_id,
        "name": name,
        "email": email,
        "country": country,
        "password_hash": hash_password(password),
        "purpose": purpose
    }

    users[email] = user
    next_user_id += 1
    return user

# -------------------------------
# Authenticate existing user
# -------------------------------
def authenticate_user(email: str, password: str) -> dict | None:
    """
    Verifies the email and password.
    Returns the user dict if authentication is successful, else None.
    """
    user = users.get(email)
    if not user:
        return None
    if verify_password(password, user["password_hash"]):
        return user
    return None

