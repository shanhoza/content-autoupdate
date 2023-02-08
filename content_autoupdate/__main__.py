import asyncio
from loguru import logger

from content_autoupdate import config
from content_autoupdate.services import downloads
from content_autoupdate.controllers import sources


@logger.catch
async def main() -> None:
    posts = await sources.get_posts()
    posts_with_source_urls = await sources.get_sources_info(posts)
    await downloads.download_files_from_posts(posts_with_source_urls) 


if __name__ == "__main__":
    config.configure_environment()
    try:
        asyncio.run(main())
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
    finally:
        config.complete_logger()

