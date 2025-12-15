# src/utils/uuid_utils.py
import uuid

def generate_uuid() -> str:
    """
    Generates a new UUID4 string.
    
    Returns:
        str: A randomly generated UUID as a string.
    """
    return str(uuid.uuid4())
