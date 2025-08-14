from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{os.getenv('AUTH0_DOMAIN')}/authorize",
    tokenUrl=f"{os.getenv('AUTH0_DOMAIN')}/oauth/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/jwks.json",
            algorithms=["RS256"],
            audience=os.getenv("AUTH0_CLIENT_ID")
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except jwt.JWTError:
        raise credentials_exception