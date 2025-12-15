# src/routers/models/user_models.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import Form

# -------------------------------
# 1. Signup Model
# -------------------------------
class SignupModel(BaseModel):
    name: str
    email: EmailStr
    country: str
    password: str
    purpose: Optional[str] = None  # Optional purpose for user

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: EmailStr = Form(...),
        country: str = Form(...),
        password: str = Form(...),
        purpose: Optional[str] = Form(None)
    ):
        return cls(
            name=name,
            email=email,
            country=country,
            password=password,
            purpose=purpose
        )

# -------------------------------
# 2. Login Model
# -------------------------------
class LoginModel(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)

# -------------------------------
# 3. User Response Model
# -------------------------------
class UserResponseModel(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    message: str
