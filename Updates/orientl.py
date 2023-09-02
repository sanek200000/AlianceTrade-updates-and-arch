from loguru import logger
from zipfile import ZipFile
from support import download_file, kill_proc, rmfile
from conf import IS_ORIENTL, ORIENTL_URL, ORIENTL_PATH


@logger.catch
def unzip(path, file_name) -> bool | None:
    zip = ZipFile(file_name)
    try:
        zip.extractall(path=path)
        logger.info(f"Файл {file_name} распакован в папку {path}")
        return True
    except Exception as ex:
        logger.opt(exception=True).debug('Exception logged with debug level:')


@logger.catch
def main():
    logger.info("-=Start update ORIENTL=-")

    if IS_ORIENTL:
        file_name = "orientl.zip"
        downloading = download_file(ORIENTL_URL, file_name)
    else:
        logger.debug("orientl отключен в ini-файле.")
        return

    if downloading:
        kill_proc(name="orientl.exe")
        unpacking = unzip(ORIENTL_PATH, file_name)
    else:
        return

    if unpacking:
        rmfile(file_name)


if __name__ == "__main__":
    main()
