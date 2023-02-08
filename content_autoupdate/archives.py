import asyncio
from time import perf_counter
from config import DOWNLOAD_DIRECTORY
import pyunpack
from pathlib import Path


def unpack_archive(archive: Path, upack_directory: Path = Path("temp")):
    return pyunpack.Archive(archive).extractall(
        directory=upack_directory / archive.name,
        auto_create_dir=True
    )


async def prepare_archives(directory: Path = DOWNLOAD_DIRECTORY):
    t1_start = perf_counter()
    DOWNLOAD_DIRECTORY = Path("dump_downloads")

    await asyncio.gather(*(
        asyncio.to_thread(unpack_archive, file)
        for file in DOWNLOAD_DIRECTORY.glob("*[!.exe]") if file.name != "view"
    ))

    t1_end = perf_counter()
    print(f"Async: {t1_end - t1_start}")


if __name__ == "__main__":
    asyncio.run(prepare_archives())
