import asyncio
import orientl
import ved_info
from loguru import logger

logger.add("updates.log", rotation="10 MB",
           backtrace=True, diagnose=False, enqueue=True)


@logger.catch
async def main():
    await asyncio.gather(
        asyncio.to_thread(ved_info.main),
        asyncio.to_thread(orientl.main))


if __name__ == "__main__":
    asyncio.run(main())
