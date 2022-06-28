from datetime import datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from . import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_drone_id(username: str, password: str) -> int | None:
    """
    Return the drone ID if the authentication is successful
    """
    if username == config.USERNAME and password == config.PASSWORD:
        return config.DRONE_ID
    return None


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + config.TOKEN_EXPIRE_MINUTES
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def _authenticate_token(token: str) -> int:
    """
    It makes this function easier to test because it is not necessary to override
    Depends(oath2_scheme)
    """
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        drone_id = int(payload['sub'])
    except (ValueError, InvalidTokenError):
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },  # OAuth spec requires this header
        )
    return drone_id


def authenticate_token(token: str = Depends(oauth2_scheme)) -> int:
    return _authenticate_token(token)
