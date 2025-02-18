from http import HTTPMethod
from urllib.parse import urljoin
from utils.classes.exceptions import InvalidLibArg

import aiohttp
import httpx
from httpx import Response
from typing import Optional, Any


class BaseClient:
    def __init__(self,
                 base_url: str,
                 client_httpx: Optional[httpx.AsyncClient],
                 session_aio: Optional[aiohttp.ClientSession]):
        self.base_url = base_url
        self.client_httpx = client_httpx
        self.session_aio = session_aio

    async def _request(self,
                       lib: str,
                       method: HTTPMethod,
                       endpoint: str,
                       data: Optional[dict] = None,
                       **kwargs) -> aiohttp.ClientResponse | Response:
        """

        :param lib: library to make request with (aio for aiohttpx & httpx for httpx)
        :param method: GET|POST (yet only available)
        :param endpoint: endpoint that connects to base url like |DOMAIN/ENDPOINT|
        :param data: data to POST
        :param kwargs: will write later
        :return:
        response: aiohttp.ClientResponse OR httpx.Response
        """
        url = urljoin(self.base_url, endpoint)
        match lib:
            case "aio":
                if data:
                    response = await self.session_aio.request(method=method, url=url, data=data, **kwargs)
                else:
                    response = await self.session_aio.request(method=method, url=url, **kwargs)
                return response

            case "httpx":
                response = await self.client_httpx.request(method=method, url=url, json=data, **kwargs)
                return response
            case _:
                raise InvalidLibArg('Invalid value of an argument \'lib\', please use either \'aio\' or \'httpx\'')

    async def get(self, lib: str, endpoint: str, params: Optional[dict] = None, **kwargs):
        """
        get method
        :param lib: supports either 'aio' for aiohttp or 'httpx' for httpx
        :param endpoint: endpoint to get
        :param params: will write later prob
        :param kwargs: will write later prob
        :return: awaits protected method and returns aiohttp.ClientResponse or httpx.Response
        """
        return await self._request(lib=lib, method=HTTPMethod.GET, endpoint=endpoint, data=None, params=params, **kwargs)

    async def post(self, lib: str, endpoint: str, data: dict[str, Any], **kwargs):
        """
        POST method (& I don't even know if it works)
        :param lib: supports either 'aio' for aiohttp or 'httpx' for httpx
        :param endpoint: endpoint to post to
        :param data: data to post: dict[str, Any]
        :param kwargs: will write later
        :return: awaits protected method and returns aiohttp.ClientResponse or httpx.Response
        """
        return await self._request(lib=lib, method=HTTPMethod.POST, endpoint=endpoint, data=data, **kwargs)