import asyncio

import pytest_asyncio
from aiohttp import ClientSession



@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='make_post_request')
def make_post_request(aiohttp_session: ClientSession):
    async def inner(endpoint, service_url, json, headers=None):
        url = f"{service_url}{endpoint}"
        async with aiohttp_session.post(url, json=json, headers=headers) as response:
            json_data, status_code = await response.json(), response.status
        return json_data, status_code
    return inner
