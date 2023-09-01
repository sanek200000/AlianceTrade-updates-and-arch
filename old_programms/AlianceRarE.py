# -*- coding: utf-8 -*-
import os
import time
import configparser
import logging
# import multiprocessing
import threading

# Описание логгирования
logging.basicConfig(
    filename="updates.log",
    format = "%(asctime)s | %(levelname)s: %(message)s",
    level=logging.INFO,
    filemode="w"
)
logging.info("______Запуск программы AlianceRarE______")

# Описание INI файла
config_path = os.path.abspath(".\conf.ini")
logging.info(f"Путь к ini файлу: {config_path}")
config = configparser.ConfigParser()
config.read(config_path)


def get_dirs():
    paths = [e.strip() for e in config.get('paths', 'path1').split(";")]

    files_dict = {}
    for dir in paths:   # Перебор путей в ini-файле
        for root, dirs, files in os.walk(dir):  # Расшариваем папки и файлы в рутовом каталоге dir

            my_list_files = []
            for file in files:
                if file.endswith(config.get('DEFAULT', 'ends')):
                    my_list_files.append(os.path.join(root, file))
                files_dict[root] = my_list_files

    return files_dict

def arch_files(files_dict):
    threads = config.get('DEFAULT', 'threads')
    sem = threading.Semaphore(int(threads))
    for target_dir, source in files_dict.items():
        if not source:
            logging.error(f"В папке {target_dir} нет файлов для архивации")
        else:
            # thr = multiprocessing.Process(target= threading_rar, args= (target_dir, source))
            thr = threading.Thread(target=threading_rar, args=(target_dir, source, sem))
            thr.start()
    thr.join()

            # target = target_dir + os.sep + time.strftime('%Y.%m.%d_%H-%M-%S') + '.rar'
            # newsource = []
            # tr = os.path.abspath(target)
            # for item in source:
            #     rar_command = config.get('DEFAULT', 'rarexe') + ' {0} {1}'.format(target, item)
            #     logging.info(f"Команда для WinRAR: {rar_command}")
            #     if os.system(rar_command) == 0:
            #         newsource.append(item.split("\\")[-1])
            #     else:
            #         logging.error("Создание резервной копии НЕ УДАЛОСЬ")
            # logging.info(f"Резервная копия файлов: {', '.join(newsource)} успешно записана в {tr}")
            # time.sleep(0.5)

def threading_rar(target_dir, source, sem):
    with sem:
        # target = target_dir + os.sep + time.strftime('%Y.%m.%d_%H-%M-%S') + '.rar'
        target = target_dir + os.sep + time.strftime('%Y.%m.%d_%H-%M-%S') + '.zip'
        newsource = []
        tr = os.path.abspath(target)
        for item in source:
            rar_command = config.get('DEFAULT', 'rarexe') + ' {0} {1}'.format(target, item)
            logging.info(f"Команда для архивации: {rar_command}")
            if os.system(rar_command) == 0:
                newsource.append(item.split("\\")[-1])
            else:
                logging.error("Создание резервной копии НЕ УДАЛОСЬ")
            logging.info(f"Резервная копия файлов: {', '.join(newsource)} успешно записана в {tr}")
        time.sleep(0.5)


if __name__ == '__main__':
    arch_files(get_dirs())
    logging.info("Конец программы AlianceRarE\n\n")
