from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException
from ..database import db

oauth2_scheme = OAuth2PasswordBearer("/token")
router = APIRouter()

user_collection = db.users



def get_user(username):
    userData = list(user_collection.find({'username':username}))
    if userData:
        return userData[0]["hashed_password"]


def verify_password(plane_pass, heshed_pass):
    return plane_pass == heshed_pass


def authenticate_user(username, password):
    user = get_user(username)
    if not user:
        raise HTTPException(status_code = 401, 
                            detail= "login error",
                            headers= {
                                "WWWW-Authenticate": "Bearer"
                            }
                            )
    if not verify_password(password, user):
        raise HTTPException(status_code = 401, 
                            detail= "login error",
                            headers= {
                                "WWWW-Authenticate": "Bearer"
                            }
                            )
    return user
        
        


@router.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    return {
        "access_token": "tomatito",
        "token_type": "bearer"
    }
   
    