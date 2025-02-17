import asyncio
import time
from utils.classes.base_class import BaseClient
import aiohttp
import httpx
# from utils.classes.aio_base_class import AIOHTTPBaseClass
# from utils.classes.httpx_base_client import HTTPXBaseClient

urls: list = [
    "/api/v2/pokemon/ditto",
    "/api/v2/pokemon/bulbasaur",
    "/api/v2/pokemon/metapod"
]


async def main():
    async with httpx.AsyncClient() as client_x, aiohttp.ClientSession() as session_aio:
        base = BaseClient(base_url="https://pokeapi.co", client_httpx=client_x, session_aio=session_aio)
        tasks_x: list = [base.get(lib='httpx', endpoint=url) for url in urls]
        tasks_aio: list = [base.get(lib='aio', endpoint=url) for url in urls]

        time_start_x = time.time()
        await asyncio.gather(
            *tasks_x
        )
        print(f"time(unite: httpx) = {time.time() - time_start_x}")
        time_start_aio = time.time()
        await asyncio.gather(
            *tasks_aio
        )
        print(f"time(unite: aio) = {time.time() - time_start_aio}")


if __name__ == "__main__":
    asyncio.run(main())
