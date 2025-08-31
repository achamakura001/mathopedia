from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.exc import UnknownHashError
import os

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import create_access_token, get_current_user, SECRET_KEY

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email
    )
    user.set_password(user_data.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse(**user.to_dict())


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    print(user_data)
    print(user.email,user.password_hash)
    print(user.check_password(user_data.password))
    # Verify password with improved error handling
    try:
        if not user.check_password(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # If password was updated from old format, save changes
        # if user.update_password_hash_if_needed(user_data.password):
        #     db.commit()
            
    except UnknownHashError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password verification error. Please contact support."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication error. Please try again."
        )
    
    print(f"🔍 User {user.email} authenticated successfully.")
    # Create access token - Make sure user_id is a string
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": str(user.id)}, 
    #     expires_delta=access_token_expires
    # )
    access_token = create_access_token(
        data={"sub": str(user.email)},
        expires_delta=access_token_expires
    )

    print(f"🔍 Login successful for user: {user.email} (ID: {user.id})")
    print(f"🔍 Created token with sub: {str(user.email)}")
    print(f"🔍 Token: {access_token[:50]}...")
    print(UserResponse(**user.to_dict()))
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=access_token_expires.microseconds,
        user=UserResponse(**user.to_dict())
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.to_dict())


@router.put("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify current password
    try:
        if not current_user.check_password(current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
    except UnknownHashError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password verification error. Please contact support."
        )
    
    # Set new password
    current_user.set_password(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


# Test endpoint to verify token
@router.get("/verify-token")
def verify_token(current_user: User = Depends(get_current_user)):
    """Test endpoint to verify JWT token is working"""
    return {
        "message": "Token is valid",
        "user_id": current_user.id,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    }