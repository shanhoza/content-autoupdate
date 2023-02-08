from typing import Iterable, TypeVar, Awaitable

import aiofiles
import httpx
from loguru import logger
from tqdm.asyncio import tqdm

import config
from controllers.sources import Post


_T = TypeVar("_T")


async def download_files_from_posts(posts: Iterable[Post]) -> None:
    logger.info("Fetching files from sources...")
    config.DOWNLOAD_DIRECTORY.mkdir(exist_ok=True)

    tasks = [_fetch_file(post) for post in posts]
    await _tick_progress_bar(tasks)


async def _fetch_file(post: Post) -> None:
    """Async fetch file if not exist"""
    async with (
        httpx.AsyncClient() as client,
        client.stream(
            method="GET", 
            url=post.source_download_url,
            follow_redirects=True) as response,
    ):
        file_ext = _get_file_extension(response.headers.get('Content-Type'))
        post.file_name = _get_file_name(post.slug_title, file_ext)
        
        if (config.DOWNLOAD_DIRECTORY / post.file_name).exists():
            logger.info(f"Found existing {post.file_name}")
            return
        
        async with aiofiles.open(
                config.DOWNLOAD_DIRECTORY / post.file_name, "wb") as file:
            if response.status_code != httpx.codes.OK:
                logger.warning(f"{response.url} ended with {response.status_code}")
                return
            async for chunk in response.aiter_bytes():
                await file.write(chunk)

    logger.info(f"Downloaded {post.file_name}")


async def _tick_progress_bar(elements: Iterable[Awaitable[_T]]) -> None:
    for func in tqdm.as_completed(
        elements, 
        desc="Total downloaded", 
        colour="green", 
        dynamic_ncols=True,
    ):
        await func


def _get_file_extension(content_type: str) -> config.POSSIBLE_FILE_EXTENSIONS:
    match content_type.split('/')[1]:
        case 'x-rar-compressed' | 'rar':
            return 'rar'
        case 'x-zip-compressed' | 'zip' | 'octet-stream':
            return 'zip'
        case _:
            return 'exe'


def _get_file_name(name: str, extension: str) -> Post.file_name:
    return f'{name}.{extension}'
