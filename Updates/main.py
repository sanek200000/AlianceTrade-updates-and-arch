import ved_info
import orientl
from loguru import logger

logger.add("updates.log", rotation="10 MB", backtrace=True, diagnose=False)


if __name__ == "__main__":
    ved_info.main()
    orientl.main()
