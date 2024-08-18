from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import db
from app.auth.auth_handler import create_access_token, verify_password, get_password_hash

oauth2_scheme = OAuth2PasswordBearer("/token")
router = APIRouter()

user_collection = db.users

def get_user(username: str):
    userData = user_collection.find_one({'username': username})
    if userData:
        return userData
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/token", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer","username":user["username"], "role":user["role"]}
