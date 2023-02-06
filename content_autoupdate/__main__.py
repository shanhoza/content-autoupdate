import asyncio
from loguru import logger

from content_autoupdate import config, sources


@logger.catch
async def main() -> None:
    posts = sources.get_posts_info()
    posts = await sources.get_info_from_sources(posts)
    write(posts, "posts.json") # вынести в другой слой
    await download_files(posts) # Скрыть детали реализации функции (await убрать)


if __name__ == "__main__":
    config.configure_environment()
    try:
        asyncio.run(main())
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
    finally:
        config.complete_logger()
