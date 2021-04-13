from passlib.context import CryptContext
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

import base64

SECRET_KEY = "FloodAppSecretKey"

ALGORITHM = "HS512"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

def extract_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        username = payload.get('sub')
        exp = payload.get('exp')
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return username