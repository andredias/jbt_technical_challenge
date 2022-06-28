import pytest
from fastapi import HTTPException

from jbt_drone import config
from jbt_drone.authentication import (
    _authenticate_token,
    create_access_token,
    get_drone_id,
)


def test_get_drone_id() -> None:
    assert get_drone_id(config.USERNAME, config.PASSWORD) == config.DRONE_ID
    assert get_drone_id(config.USERNAME + 'x', config.PASSWORD) is None
    assert get_drone_id(config.USERNAME, config.PASSWORD + 'x') is None


def test_token() -> None:
    drone_id = 1234
    token1 = create_access_token({'sub': drone_id})
    token2 = create_access_token({'sub': drone_id})

    assert len(token1) == len(token2)
    assert len(token1) > 0

    assert _authenticate_token(token1) == _authenticate_token(token2) == drone_id


def test_authentication() -> None:
    token = create_access_token({'sub': 1234})
    assert _authenticate_token(token) == 1234
    with pytest.raises(HTTPException):
        assert _authenticate_token('not valid token') == 1234
