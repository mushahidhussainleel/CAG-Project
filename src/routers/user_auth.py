# src/routers/user_auth.py
from fastapi import APIRouter, Depends, HTTPException
from src.routers.models.user_models import SignupModel, LoginModel, UserResponseModel
from src.services.user_service import create_user, authenticate_user
from src.services.jwt_service import create_access_token

router = APIRouter()

# -------------------------------
# 1. User Signup 
# -------------------------------
@router.post("/signup", response_model=UserResponseModel)
def signup(user: SignupModel = Depends(SignupModel.as_form)):
    try:
        new_user = create_user(
            name=user.name,
            email=user.email,
            country=user.country,
            password=user.password,
            purpose=user.purpose
        )
        return {
            "user_id": new_user["user_id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "message": "User registered successfully!"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------
# 2. User Login
# -------------------------------
@router.post("/login")
def login(user: LoginModel = Depends(LoginModel.as_form)):
    authenticated_user = authenticate_user(user.email, user.password)

    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_data = {
        "user_id": authenticated_user["user_id"],
        "email": authenticated_user["email"]
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful!"
    }
