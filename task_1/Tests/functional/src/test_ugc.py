import pytest
from functional.settings import test_settings
import uuid
import time

user_create = {
            "login": "test_login",
            "password": "test_password",
            "email": "test_email"}

user_login = {
            "login": "test_login",
            "password": "test_password",
            "agent": "test_device"}

@pytest.mark.parametrize(
    'in_data, out_data',
    [
        (
                {
                    "action": "test_action",
                    "film_id": str(uuid.uuid4()),
                },
                {'status_code': 200},
        ),
        (
                {
                    "action": "test_action",
                    "film_id": str(uuid.uuid4()),
                },
                {'status_code': 200},
        ),
    ]
)
@pytest.mark.asyncio
async def test_ugc(make_post_request, in_data, out_data):
    body, status = await make_post_request(endpoint="/api/v1/auth/registration", service_url=test_settings.auth_service_url, json=user_create)
    body, status = await make_post_request(endpoint="/api/v1/auth/login", service_url=test_settings.auth_service_url, json=user_login)
    if not body:
        raise BrokenPipeError
    token = body['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    body, status = await make_post_request(endpoint="/api/v1/action", service_url=test_settings.ugc_service_url, json=in_data, headers=headers)
    assert status == out_data['status_code']
