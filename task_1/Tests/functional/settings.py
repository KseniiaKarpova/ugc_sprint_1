from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    auth_service_url: str = Field('http://test_auth_api:9999', env='AUTH_SERVICE_URL')
    ugc_service_url: str = Field('http://test_ugc_api:7075', env='UGC_SERVICE_URL')


test_settings = TestSettings()
