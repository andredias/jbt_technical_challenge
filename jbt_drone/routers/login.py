from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..authentication import create_access_token, get_drone_id
from ..schemas import Token

router = APIRouter(prefix='/login', tags=['authentication'])


@router.post('', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    drone_id = get_drone_id(form_data.username, form_data.password)
    if not drone_id:
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token({'sub': drone_id})
    return {'access_token': access_token, 'token_type': 'bearer'}
