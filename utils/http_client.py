import requests
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import RequestException, ConnectionError
from typing import Dict, Any, Optional
import logging
from config import TIMEOUT, API_KEY, ACCESS_TOKEN
from utils.log_config import setup_logging
import io
import sys

setup_logging()
logger = logging.getLogger(__name__)

class SuppressedStdout:
    def __enter__(self):
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        return sys.stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout


class HttpClient:
    @staticmethod
    def create_retry_session(
            retries: int = 3,
            backoff_factor: float = 0.3,
            status_forcelist: tuple = (500, 502, 503, 504),
            session: Optional[requests.Session] = None
    ) -> requests.Session:
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @staticmethod
    def request(method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        headers: Dict[str, str] = kwargs.pop('headers', {})

        if ACCESS_TOKEN:
            headers['Authorization'] = f'Bearer {ACCESS_TOKEN}'
        elif API_KEY:
            headers['Authorization'] = f'Bearer {API_KEY}'
        headers['Content-Type'] = headers.get('Content-Type', 'application/json')

        session = HttpClient.create_retry_session()

        with SuppressedStdout():
            try:
                response = session.request(
                    method,
                    endpoint,
                    timeout=TIMEOUT,
                    headers=headers,
                    **kwargs
                )
                response.raise_for_status()
                logger.info(f"Successful {method} request to {endpoint}")
                return response
            except ConnectionError as e:
                logger.error(f"Connection error for {method} request to {endpoint}: {str(e)}")
                logger.error(f"Please verify the endpoint URL and network connectivity")
                raise
            except RequestException as e:
                logger.error(f"Failed {method} request to {endpoint}: {str(e)}")
                raise
            finally:
                session.close()

    @classmethod
    def get(cls, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return cls.request("GET", endpoint, params=params, **kwargs)

    @classmethod
    def post(cls, endpoint: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return cls.request("POST", endpoint, data=data, json=json, **kwargs)

    @classmethod
    def put(cls, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return cls.request("PUT", endpoint, data=data, **kwargs)

    @classmethod
    def delete(cls, endpoint: str, **kwargs: Any) -> requests.Response:
        return cls.request("DELETE", endpoint, **kwargs)

    @classmethod
    def patch(cls, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> requests.Response:
        return cls.request("PATCH", endpoint, data=data, **kwargs)

    @classmethod
    def negative_validation_test(cls, expected_status_code: int, endpoint: str,
                                 method: str, json_data: Optional[Dict] = None,
                                 params: Optional[Dict] = None) -> None:
        with SuppressedStdout():
            try:
                method_map = {
                    'GET': cls.get,
                    'POST': cls.post,
                    'PUT': cls.put,
                    'DELETE': cls.delete
                }

                if method not in method_map:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                http_method = method_map[method]
                kwargs = {'json': json_data} if json_data else {'params': params} if params else {}

                response = http_method(endpoint, **kwargs)

                logger.info(f"\nEndpoint: {endpoint}")
                logger.info(f"Method: {method}")
                logger.info(f"Status Code: {response.status_code}")

                try:
                    response_content = response.json()
                    logger.info(f"Response Content: {response_content}")
                except ValueError:
                    logger.info(f"Response Text: {response.text}")

                assert response.status_code == expected_status_code, (
                    f"Expected status code {expected_status_code}, but got {response.status_code}.\n"
                    f"Response content: {response.text}"
                )

            except HTTPError as e:
                logger.error(f"HTTP Error occurred during negative validation test:")
                logger.error(f"Status code: {e.response.status_code}")
                try:
                    error_content = e.response.json()
                    logger.error(f"Error response: {error_content}")
                except ValueError:
                    logger.error(f"Error text: {e.response.text}")
                raise

            except ConnectionError as e:
                logger.error(f"Connection error during negative validation test: {str(e)}")
                logger.error(f"URL: {endpoint}")
                raise

            except RequestException as e:
                logger.error(f"Request error during negative validation test: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Status code: {e.response.status_code}")
                    try:
                        error_content = e.response.json()
                        logger.error(f"Error response: {error_content}")
                    except ValueError:
                        logger.error(f"Error text: {e.response.text}")
                raise

            except Exception as e:
                logger.error(f"Unexpected error during negative validation test: {str(e)}")
                raise

def validate_endpoint(endpoint: str) -> bool:
    with SuppressedStdout():
        try:
            response = requests.head(endpoint, timeout=5)
            return True
        except RequestException:
            logger.error(f"Failed to validate endpoint: {endpoint}")
            return False