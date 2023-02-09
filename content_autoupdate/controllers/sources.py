import asyncio
import json
from typing import Iterable

import httpx
from fake_useragent import UserAgent
from loguru import logger

from content_autoupdate import config
from content_autoupdate.services.exceptions import CantGetPostsError
from content_autoupdate.services.posts import Post
from content_autoupdate.controllers.requests import send_request
from content_autoupdate.services.parsers import parse_site, form_api_url


async def get_posts() -> tuple[Post]:
    await send_request("POST", config.AUTH_URL, auth=(
            config.EMAIL_ADDRESS, 
            config.EMAIL_PASSWORD
        )
    )
    response = await send_request("GET", config.PUBLICATIONS_URL)
    return _parse_posts(response)


async def get_sources_info(posts: Iterable[Post]) -> list[Post]:
    headers = {
        "User-Agent": UserAgent().random,
        "X-Requested-With": "XMLHttpRequest",
    }
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [
            asyncio.create_task(_task_get_source_info(client, post))
            for post in posts
        ]
        if not tasks:
            logger.info("Tasks list is empty. Seems to be all mods are up to date")
            exit()
        logger.debug("All tasks created. Gathering sources information")
        await asyncio.gather(*tasks)
        logger.debug("Got sources download urls. Ready to start download files")
    return [post for post in posts if post.source_download_url]


def _parse_posts(response: httpx.Response) -> tuple[Post]:
    try:
        posts_dict = response.json()
    except json.JSONDecodeError:
        logger.error("Got main source url but unable to decode it")
        raise CantGetPostsError
    else:
        logger.info("Fetched posts info. Downloading files...")
        return tuple(
            Post.from_dict(post)
            for post in posts_dict.get("posts")
            if post.get("is_published") and post.get("supported_wot_version") != config.ACTUAL_WOT_VERSION
        )


async def _task_get_source_info(client: httpx.AsyncClient, post: Post) -> Post:
    url, url_domain_name = _prepare_source_connection(post.source_url)
    response = await send_request("GET", url)
    post.source_download_url = parsers.parse_site(response, url_domain_name)

    if not post.source_download_url:
        logger.info(f'Post {post.title} did not pass the version check \
                      on the source site ({post.source_url})')
        return post
    
    if post.source_download_url.startswith('https://drive.google.com'):
       post.source_download_url = _form_drive_url_to_download_url(post.source_download_url)
       
    return post


def _prepare_source_connection(url: Post.source_url) -> tuple[config.Url, str]:
    domain_name = _get_domain_name(url)
    if domain_name in config.SOURCES_CONTAINING_API_RESPONSE:
        url = parsers.form_api_url(url, domain_name)
    return url, domain_name


def _get_domain_name(url: config.Url) -> str:
    return url.split("//")[-1].split("/")[0].split("?")[0]


def _convert_google_drive_url_to_download_url(url: config.Url) -> config.Url:
    """If the source download url is a link to a google drive view, 
       it will be converted to a google drive download url"""
    file_id = url.rsplit('/', 2)[1]
    return f'https://drive.google.com/uc?id={file_id}&confirm=1'

