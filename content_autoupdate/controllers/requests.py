import httpx
import config


async def send_request(method: str, url: config.Url, **params) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        return await client.send(httpx.Request(method, url, **params))


async def send_request_stream(method: str, url: config.Url, **params) -> None:
    async with (
        httpx.AsyncClient() as client,
        client.stream(
            method=method,
            url=url,
            params=params) as response,
        aiofiles.open(directory / filename, "wb") as file
    ):
        
