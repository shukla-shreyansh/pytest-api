import pytest
from requests import HTTPError

from api.endpoints import Endpoint
from payload_data.payload_data import *
from schemas.sample_schema import SAMPLE_SCHEMA
from utils.http_client import HttpClient
from utils.schema_validator import SchemaValidator
from schemas.sample_schema import *
from config import HOST
import logging

logger = logging.getLogger(__name__)


class Test_Sample:

    @pytest.mark.sanity
    def test_sample1(self):
        endpoint = f"{HOST}{Endpoint.SAMPLE_ENDPOINT.value}"
        params = "key=abc.jpeg"
        try:
            response = HttpClient.get(endpoint,params=params)
            print("\nResponse content:", response.json())
        except HTTPError as e:
            print(f"HTTP Error occurred: {e}")
            print("Response status code:", e.response.status_code)
            print("Response content:", e.response.text)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        SchemaValidator.validate_schema(response.json(), SAMPLE_SCHEMA)
