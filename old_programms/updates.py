# -*- coding: utf-8 -*-
from zipfile import ZipFile
import requests
import os
import configparser
from time import sleep
import re
import logging

logging.basicConfig(
    filename="updates.log",
    format = "%(asctime)s | %(levelname)s: %(message)s",
    level=logging.INFO,
    filemode="a"
)
# logging.debug("This is a debug message")
logging.info("____Запуск программы UPDATES____")
# logging.error("An error has happened!")

config_path = os.path.abspath(".\conf.ini")
config = configparser.ConfigParser()
config.read(config_path)

headers = {
    "Accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

def download_file(url, fname):
    try:
        file = open(rf'.\{fname}', "wb") #открываем файл для записи, в режиме wb
        ufr = requests.get(url) #делаем запрос
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
        file.close()
        logging.info(f"Файл {fname} по адресу {url} скачан")
    except Exception:
        logging.error(f"Такого адреса {url} не существует")
        exit()

def kill_proc(proc_name):
    try:
        os.system(f"taskkill /f /im  {proc_name}")
        logging.info(f"Процесс {proc_name} остановлен")
        sleep(2)
    except Exception:
        logging.info(f"Нет запущеных процессов {proc_name}")

def unzip(path, fname):
    zip = ZipFile(rf'.\{fname}')
    try:
        zip.extractall(path=path)
        logging.info(f"Файл {fname} распакован в папку {path}")
    except Exception:
        logging.error("Ошибка! Процесс orientl.exe запущен, остановите его.")

def rmfile(fname):
    try:
        os.remove(rf'.\{fname}')
        logging.info(f"Файл {fname} удален")
    except OSError:
        pass

def ved_info_ver(path):
    config_path = os.path.abspath(path)
    config = configparser.ConfigParser()
    config.read(config_path)
    return config.get('StationSetup', 'ALIANCE')

def parsing(url, version):
    req = requests.get(url, headers=headers)
    src = req.text

    result = re.findall(rf"vif{version}f\d\d.rnw\<", src)
    try:
        src = result[-1][:-1]
    except Exception:
        src = "Null"
    return src

def seek_and_destroy():
    for file in os.listdir(".\\"):
        if file.endswith(".rnw"):
            rmfile(os.path.join(file))


if __name__ == '__main__':
    prog_orientl = config.get('DEFAULT', 'orientl')
    prog_ved = config.get('DEFAULT', 'ved_info')

    if prog_ved == '0' and prog_ved == '0':
        logging.error("Не выделена ни одна из программ")

    if prog_orientl == '1':
        logging.info("Начало блока для ORIENTL")
        url = config.get('orientl', 'url')
        path = config.get('orientl', 'path')
        fname = 'orientl.zip'
        proc_name = 'orientl.exe'

        download_file(url, fname)
        kill_proc(proc_name)
        unzip(path, fname)
        rmfile(fname)
        logging.info("Конец блока для ORIENTL\n")

    if prog_ved == '1':
        logging.info("Начало блока для VED_INFO")
        ved_ini = config.get('ved_info', 'ved_ini')
        url = config.get('ved_info', 'url')

        version = ved_info_ver(ved_ini).split('.')[-1]
        logging.info(f"Нонешняя версия вэд-инфо {version}")
        proc_name = 'ved_info.exe'
        seek_and_destroy()

        fname = parsing(url, version)
        if fname == 'Null':
            logging.error('Нет новых обновлений ved_info')
        else:
            download_file(url + fname, fname)
            kill_proc(proc_name)
            os.startfile(rf'.\{fname}')
        logging.info("Конец блока для VED_INFO\n")

