import configparser
from os.path import abspath
from loguru import logger


# Инициализация ini-фавйла
conf_ini_path = abspath("conf.ini")
config = configparser.ConfigParser()
config.read(conf_ini_path, encoding="cp1251")


# VED_INFO
@logger.catch
def get_version(path: str) -> str | None:
    """Get version of ved_info from `instcfg.ini`

    Args:
        path (str): path to instcfg.ini by Ved_info

    Returns:
        str: current program version
    """
    try:
        config = configparser.ConfigParser()
        config.read(path, encoding="1251")
        return config.get("StationSetup", "ALIANCE").strip().split(".")[-1]
    except Exception as ex:
        logger.opt(exception=True).debug('Exception logged with debug level:')


IS_VEDINFO = int(config.get("DEFAULT", "ved_info").strip())
VEDINFO_INI = config.get("VED_INFO", "ved_ini").strip()
VEDINFO_FTP = config.get("VED_INFO", "url").strip()
# TODO не забудь поменять путь на VEDINFO_INI перед компиляцией
VEDINFO_VER = get_version('instcfg.ini')

# ORIENTL
IS_ORIENTL = int(config.get("DEFAULT", "orientl").strip())
ORIENTL_URL = config.get("ORIENTL", "url").strip()
ORIENTL_PATH = config.get("ORIENTL", "path").strip()

if __name__ == "__main__":
    print("conf_ini_path =", conf_ini_path)
    print("IS_VEDINFO   ", IS_VEDINFO)
    print("VEDINFO_INI   ", VEDINFO_INI)
    print("VEDINFO_FTP   ", VEDINFO_FTP)
    print("VEDINFO_VER   ", VEDINFO_VER)
    print("IS_ORIENTL   ", IS_ORIENTL)
    print("ORIENTL_URL   ", ORIENTL_URL)
    print("ORIENTL_PATH   ", ORIENTL_PATH)
