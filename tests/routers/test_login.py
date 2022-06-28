from httpx import AsyncClient

from jbt_drone import config


async def test_login(client: AsyncClient) -> None:
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {'username': config.USERNAME, 'password': config.PASSWORD}
    response = await client.post('/login', data=data, headers=headers)
    assert response.status_code == 200
    assert set(response.json().keys()) == set(['access_token', 'token_type'])

    data['password'] = 'ForaBolsonaro'
    response = await client.post('/login', data=data, headers=headers)
    assert response.status_code == 401
    assert 'detail' in response.json()
