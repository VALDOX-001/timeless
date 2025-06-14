from fastapi import Depends, HTTPException, status
from models import User, UserRole
from routes.auth import get_current_user

def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    return current_user

def customer_only(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.customer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access only"
        )
    return current_user
