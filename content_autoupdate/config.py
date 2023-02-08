import os
from pathlib import Path
from typing import TypeAlias, Literal

from dotenv import load_dotenv
from loguru import logger
from tqdm.asyncio import tqdm
import asyncio

load_dotenv()

Url: TypeAlias = str
LOGGER_LEVEL = "DEBUG"

# mods settings
ACTUAL_WOT_VERSION = "1.18.1.2"
DOWNLOAD_DIRECTORY = Path("data/downloads")
LOGS_DIRECTORY = Path("data/logs")
POSSIBLE_FILE_EXTENSIONS: TypeAlias = Literal['rar', 'zip', 'exe']

# auth stuff
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS") 
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
AUTH_URL = "https://modsfortanks.ru/api/auth/login"
PUBLICATIONS_URL = "https://modsfortanks.ru/api/posts?categorySlug=all" \
                   "&withDrafts=true&limit=999&orderBy=source_url"

# sources that provides api
SOURCES_CONTAINING_API_RESPONSE = (
    "wgmods.net",
    "protanki.tv",
)


def configure_environment():
    logger.remove()
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
    logger.debug("Initializing logger")
    logger.add(
        f"{LOGS_DIRECTORY}\\debug.zip",
        format="{time} {level} {message}",
        level=LOGGER_LEVEL,
        rotation="10:00",
        enqueue=True,
    )


def complete_logger() -> None:
    asyncio.run(_async_complete_logger())

async def _async_complete_logger() -> None:
    await logger.complete()
