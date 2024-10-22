from enum import Enum
from json import JSONDecodeError
from typing import Literal

import requests
from requests.auth import AuthBase

class ContentType(Enum):
    WEB_FORM = "web_form"
    JSON = "json"
    XML = "xml"

class JWTAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self._auth = None
        self._cookies = None
        self._connection_timeout = 5
        self._read_timeout = 5
        self._method_map = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete
        }

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, new_url: str):
        self._base_url = new_url

    @property
    def connection_timeout(self):
        return self._connection_timeout

    @connection_timeout.setter
    def connection_timeout(self, new_connection_timeout):
        self.connection_timeout = new_connection_timeout

    @property
    def read_timeout(self):
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, new_read_timeout):
        self._read_timeout = new_read_timeout

    def set_authorization(self, credentials: tuple[str, str] = None, token: str = None):
        if credentials is not None:
            username, password = credentials
            self._auth = (username, password)
        if token is not None:
            self._auth = JWTAuth(token)

    def set_cookies(self, cookies: dict):
        self._cookies = cookies

    def _request(self, http_method_name: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
                 endpoint: str, params: dict, payload: dict | str = None, content_type: ContentType = None) -> tuple:
        data = None
        if not content_type and not payload:
            data = (self._method_map[http_method_name](
                url=self._base_url + endpoint, params=params, auth=self._auth,
                cookies=self._cookies, timeout=(self.connection_timeout, self.read_timeout)
                )
            )
        elif content_type.value == content_type.WEB_FORM:
            data = (self._method_map[http_method_name](
                    url=self._base_url+endpoint, data=payload,
                    params=params, auth=self._auth, cookies=self._cookies,
                    timeout=(self.connection_timeout, self.read_timeout)
                    )
            )
        elif content_type.value == content_type.JSON:
            data = (self._method_map[http_method_name](
                    url=self._base_url+endpoint, json=payload,
                    params=params, auth=self._auth, cookies=self._cookies,
                    timeout=(self.connection_timeout, self.read_timeout)
                    )
            )
        elif content_type.value == content_type.WEB_FORM:
            data = (self._method_map[http_method_name](
                    url=self._base_url+endpoint, data=payload, headers={"content-type": "application/xml"},
                    params=params, auth=self._auth, cookies=self._cookies,
                    timeout=(self.connection_timeout, self.read_timeout)
                    )
            )
        return HttpClient._handle_response(data)

    @classmethod
    def _handle_response(cls, response) -> tuple:
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(f"HTTP error occurred: {error}")
            return ()
        else:
            if response.headers["content-type"] == "application/json":
                try:
                    return response.status_code, response.json()
                except JSONDecodeError as error:
                    print(f"JSON decode error occurred: {error}")
                    return ()
            else:
                return response.status_code, response.text

    def get(self, endpoint: str, params: dict=None) -> tuple:
        return self._request(http_method_name="GET", endpoint=endpoint, params=params)

    def post(self, endpoint: str, payload: dict | str, content_type: ContentType, params: dict=None) -> tuple:
        return self._request(http_method_name="POST", endpoint=endpoint, payload=payload, params=params, content_type=content_type)

    def put(self, endpoint: str, payload: dict | str, content_type: ContentType, params: dict = None) -> tuple:
        return self._request(http_method_name="PUT", endpoint=endpoint, payload=payload, params=params, content_type=content_type)

    def patch(self, endpoint: str, payload: dict | str, content_type: ContentType, params: dict = None) -> tuple:
        return self._request(http_method_name="PATCH", endpoint=endpoint, payload=payload, params=params, content_type=content_type)

    def delete(self, endpoint: str, params: dict = None) -> tuple:
        return self._request(http_method_name="DELETE", endpoint=endpoint, params=params)
