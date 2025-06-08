#!/bin/python

# system lib
from hashlib import md5
from os import listdir, makedirs
from os.path import basename, exists, getctime, isdir, isfile, join, splitext
from shutil import copytree
from sys import platform
from time import strftime

# third part lib
from toml import load as load_toml

# define
backup_folder = "saves"
max_file = 1024 * 1024 * 10
DEBUG = False


class GameConfig:
    """游戏配置"""

    class __config_base:
        path = ""
        config = ""
        download = ""

    class __config_game:
        name = ""
        name_zh_cn = ""
        platform = ""
        path = ""
        exe_path = ""
        save_path = ""
        save_latest: bool = False
        is_folder: bool = False

    def __init__(self, folder_name: str = "none", config_file: str = "config.toml"):
        self.base = self.__config_base()
        self.game = self.__config_game()
        self.load_config(folder_name, config_file)
        pass

    def __str__(self) -> str:
        return (
            "{\n"
            + "    game: {\n"
            + f"        name:      {self.game.name}\n"
            + f"        name_zh:   {self.game.name_zh_cn}\n"
            + f"        platform:  {self.game.platform}\n"
            + f"        path:      {self.game.path}\n"
            + f"        exe_path:  {self.game.exe_path}\n"
            + f"        save_path: {self.game.save_path}\n"
            + f"        latest:    {self.game.save_latest}\n"
            + f"        is_folder: {self.game.is_folder}\n"
            + "    }\n"
            + "    base: {\n"
            + f"        path:      {self.base.path}\n"
            + f"        config:    {self.base.config}\n"
            + f"        download:  {self.base.download}\n"
            + "    }\n"
            + "}"
        )

    def set_from(self, data: dict):
        try:
            self.game.name = data["game"]["name"]
            self.game.name_zh_cn = data["game"]["name-zh-cn"]
            self.game.platform = data["game"]["platform"]
            self.game.path = data["game"]["path"]
            self.game.exe_path = data["game"]["exe_path"]
            self.game.save_path = data["game"]["save_path"]
            self.game.save_latest = data["game"]["save_latest"]
            self.base.download = data["base"]["download"]
        except Exception:
            raise "data is wrong"

    def check(self) -> bool:
        if not self.game.name:
            print(f"[ERROR] not game name in {join(self.base.path, self.base.config)}")
            return False
        if not self.game.name_zh_cn:
            print(f"[ERROR] not game name zh-cn in {join(self.base.path, self.base.config)}")
            return False
        if not self.game.platform:
            print(f"[ERROR] not game platform in {self.game.name}")
            return False
        if not self.game.save_path or not isdir(self.game.save_path):
            print(f"[ERROR] not game save path in {self.game.name}")
            return False
        if not self.base.path or not isdir(self.base.path):
            print(f"[ERROR] not base path in {self.game.name}")
            return False
        if not self.game.path or not isdir(self.game.path):
            print(f"[WRONG] not game path in {self.game.name}")
        if not self.game.exe_path or not isfile(self.game.exe_path):
            print(f"[WRONG] not game exe path in {self.game.name}")
        return True

    def load_config(self, folder_name: str = "none", config_file: str = "config.toml"):
        """
        加载并解析 TOML 配置文件\n
        folder_name: 文件夹名
        """
        self.base.path = join(backup_folder, folder_name)
        config_path = join(self.base.path, config_file)
        if not exists(join(self.base.path, config_file)):
            raise FileNotFoundError(f"{config_path} is not exist")
        self.base.config = config_file
        with open(config_path, encoding="utf-8") as file:
            self.set_from(load_toml(file))


def get_all_file(orgin: str, file_list: list[str], dir: str = "") -> list[str]:
    if isfile(join(orgin, dir)):
        file_list.append(dir)
    elif isdir(join(orgin, dir)):
        for f in listdir(join(orgin, dir)):
            get_all_file(orgin, file_list, join(dir, f))
    return file_list


def is_same(dir1: str, dir2: str) -> bool:
    list1 = get_all_file(dir1, [])
    list2 = get_all_file(dir2, [])
    if len(list1) != len(list2):
        return False
    if "".join(list1) != "".join(list2):
        return False

    md5_1, md5_2 = [], []
    for file in list1:
        with open(join(dir1, file), "br") as f:
            md5_1.append(str(md5(f.read()).hexdigest()))
    for file in list2:
        with open(join(dir2, file), "br") as f:
            md5_2.append(str(md5(f.read()).hexdigest()))
    return md5_1 == md5_2


def get_last_dir(dir: str, num: int = 0):
    if isdir(dir):
        dirs = [d for d in listdir(dir) if isdir(join(dir, d))]
        dirs.sort(key=lambda fn: getctime(dir + "\\" + fn), reverse=True)
        if len(dirs) > num:
            return join(dir, dirs[num])
        else:
            return ""
    else:
        return ""


def backup_save_files(config: GameConfig, backup_time: str = "", to_folder: bool = False):
    """根据配置备份存档文件"""
    global DEBUG
    if platform[:3] != config.game.platform[:3]:
        print(f"Not same platform, skip {config.game.name}!")
        return -1
    if backup_time == "":
        backup_time = strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = join(config.base.path, backup_time)
    last_backup_dir = get_last_dir(config.base.path)
    if config.game.save_latest:
        save_path = get_last_dir(config.game.save_path)
    else:
        save_path = config.game.save_path
    if to_folder:
        backup_dir = join(backup_dir, basename(save_path))
        last_backup_dir = join(last_backup_dir, basename(save_path))
    if last_backup_dir != "" and is_same(save_path, last_backup_dir):
        print(f"[INFO] Same saves, skip {config.game.name} ({join(config.base.path, config.base.config)})!")
    else:
        print(f"[INFO] Backup {config.game.name}:\n" + f"    {save_path}\n" + f" -> {backup_dir}")
        if not DEBUG:
            copytree(save_path, backup_dir)
            print(f"[INFO] Success!\n")


def init():
    if not isdir(backup_folder):
        makedirs(backup_folder)
    pass


def main():
    for folder in listdir(backup_folder):
        if isfile(join(backup_folder, folder)):
            continue
        files = [
            f for f in listdir(join(backup_folder, folder)) if splitext(join(backup_folder, folder, f))[1] == ".toml"
        ]
        if len(files) > 1:
            to_folder = True
            time = strftime("%Y-%m-%d_%H-%M-%S")
        else:
            to_folder = False
            time = ""
        for file in files:
            if isfile(join(backup_folder, folder, file)):
                config = GameConfig(folder, file)
                if config.check():
                    backup_save_files(config=config, backup_time=time, to_folder=to_folder)
                else:
                    print(folder, config)


if __name__ == "__main__":
    init()
    main()
