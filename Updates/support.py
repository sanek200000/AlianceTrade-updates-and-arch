import requests
import os
from time import sleep
from loguru import logger


@logger.catch
def download_file(url: str, file_name: str) -> bool:
    """
    The function accesses the server by `URL`,
    if response=200, downloads the file to the root folder named `file_name`.

    Args:
        url (str): Url name.
        file_name (str): Update name.
    Returns:
        bool: if response=200 and file downloaded, returns True.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        return True
    else:
        logger.debug("support.download_file.response =", response)
        return False


@logger.catch
def kill_proc(name: str) -> None:
    """Kill process with name: `name`

    Args:
        name (str): name of killing process
    """
    try:
        os.system(f"taskkill /f /im  {name}")
        sleep(2)
    except Exception:
        logger.debug(f"Нет запущеных процессов {name}")


@logger.catch
def rmfile(file_name):
    try:
        os.remove(rf".\{file_name}")
        logger.info(f"Файл {file_name} удален")
    except OSError as ex:
        logger.opt(exception=True).debug('Exception logged with debug level:')
