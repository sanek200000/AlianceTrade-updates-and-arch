import os
import requests
from loguru import logger
from bs4 import BeautifulSoup
from support import download_file, kill_proc, rmfile
from conf import VEDINFO_FTP, VEDINFO_VER, IS_VEDINFO


@logger.catch
def get_last_version() -> str | None:
    """
    The function gets a list of update files.
    Selects files with the required version from the list
    (links = ..., vig[06]g08.rnw, ...).
    Selects the file with the latest version from the list
    (link = vig06g[08].rnw).

    Returns:
        str: Update file name.
    """
    if VEDINFO_VER:
        response = requests.get(VEDINFO_FTP)

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all(
            "a", string=lambda text: text[3:5] == VEDINFO_VER)
        hrefs = [i.get("href") for i in links]

        if hrefs:
            link = list(
                filter(lambda text: str(max(int(i[6:8])
                                            for i in hrefs)) in text, hrefs))[0]
            return link

        logger.info(f"VEDINFO_VER = {VEDINFO_VER}")
        return None
    else:
        logger.debug(f"VEDINFO_VER = {VEDINFO_VER}")
        return None


@logger.catch
def start_update(file_name: str) -> None:
    """The function launches the update file for execution.

    Args:
        file_name (str): Update name.
    """
    try:
        version = file_name[6:8]
        os.startfile(file_name)
        logger.info(f"ved_info обновлен на версию {version}")
    except Exception as ex:
        logger.opt(exception=True).debug('Exception logged with debug level:')


@logger.catch
def main() -> None:
    logger.info("-=Start update VED_INFO=-")

    # Удаляем файлы прошлых обновлений.
    files_list = [file for file in os.listdir(r"./") if file.endswith(".rnw")]
    if files_list:
        [rmfile(f) for f in files_list]

    # Основной поток
    if IS_VEDINFO:
        file_name = get_last_version()
    else:
        logger.info("ved_info отключен в ini-файле.")
        return

    if file_name:
        url = VEDINFO_FTP + file_name
        downloading = download_file(url, file_name)
    else:
        logger.debug("На сайте нет новых обновлений.")
        return

    if downloading:
        kill_proc(name="ved_info.exe")
        start_update(file_name)
    else:
        logger.debug("Ничего не скачалось!")
        return


if __name__ == "__main__":
    main()
