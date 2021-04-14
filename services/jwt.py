from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import time
import base64

SECRET_KEY = "FloodAppSecretKey"

ALGORITHM = "HS512"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

def extract_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    username = None
    try:
        payload = jwt.decode(token, SECRET_KEY)
        username = payload.get('sub')
        exp = payload.get('exp')

        if username is None:
            print("JWT: Username = null")
            raise credentials_exception

        if exp < int (time.time()):
            print("EXP < time")
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return username