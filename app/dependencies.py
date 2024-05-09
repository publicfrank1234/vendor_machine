# app/dependencies.py
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.routers.users import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    # For simplicity, assume the token is the user_id
    # Skipped jwt token validation
    user_id = token  # Simplification for example purposes
    return int(user_id)


def seller_role_required(user_id: int = Depends(get_current_user)):
    try:
        if user_id in users:
            user = users[user_id]
            print("user role is : ", user.role)
            if user.role != "seller":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied, seller role required",
                )
            return user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        )


def buyer_role_required(user_id: int = Depends(get_current_user)):
    try:
        if user_id in users:
            user = users[user_id]
            print("user role is : ", user.role)
            if user.role != "buyer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied, buyer role required",
                )
            return users[user_id]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
        )
