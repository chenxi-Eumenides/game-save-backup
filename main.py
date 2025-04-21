#!/bin/python

from os.path import exists, isdir, isfile, join, getmtime
from os import listdir, makedirs
from shutil import copytree
from time import strftime
from hashlib import md5
from sys import platform

from toml import load as load_toml

# define
backup_folder = "saves"
DEBUG = True


class GameConfig():
    """游戏配置"""
    class __config_base():
        path = ""
        config = "config.toml"
        download = ""

    class __config_game():
        name = ""
        name_zh_cn = ""
        platform = ""
        path = ""
        exe_path = ""
        save_path = ""
        save_latest: bool = False

    def __init__(self):
        self.base = self.__config_base()
        self.game = self.__config_game()
        pass

    def __str__(self) -> str:
        return "{\n" \
            + "    game: {\n" \
            + f"        name:      {self.game.name}\n" \
            + f"        name_zh:   {self.game.name_zh_cn}\n" \
            + f"        platform:  {self.game.platform}\n" \
            + f"        path:      {self.game.path}\n" \
            + f"        exe_path:  {self.game.exe_path}\n" \
            + f"        save_path: {self.game.save_path}\n" \
            + f"        latest:    {self.game.save_latest}\n" \
            + "    }\n" \
            + "    base: {\n" \
            + f"        path:      {self.base.path}\n" \
            + f"        config:    {self.base.config}\n" \
            + f"        download:  {self.base.download}\n" \
            + "    }\n" \
            + "}"

    def set_from(self, data: dict):
        try:
            self.game.name = data['game']['name']
            self.game.name_zh_cn = data['game']['name-zh-cn']
            self.game.platform = data['game']['platform']
            self.game.path = data['game']['path']
            self.game.exe_path = data['game']['exe_path']
            self.game.save_path = data['game']['save_path']
            self.game.save_latest = data['game']['save_latest']
            self.base.download = data['base']['download']
        except:
            raise "data is wrong"

    def check(self) -> bool:
        if not self.game.name:
            print("not game name")
            return False
        if not self.game.name_zh_cn:
            print("not game name zh-cn")
            return False
        if not self.game.platform:
            print("not game platform")
            return False
        if not self.game.path or not isdir(self.game.path):
            print("not game path")
            return False
        if not self.game.exe_path or not isfile(self.game.exe_path):
            print("not game exe path")
            return False
        if not self.game.save_path or not isdir(self.game.save_path):
            print("not game save path")
            return False
        if not self.base.path or not isdir(self.base.path):
            print("not base path")
            return False
        if not self.base.config or not isfile(join(self.base.path, self.base.config)):
            print("not base path")
            return False
        return True


def load_config(folder_name: str = "none"):
    """
    加载并解析 TOML 配置文件\n
    folder_name: 文件夹名
    """
    config = GameConfig()
    config.base.path = join(backup_folder, folder_name)
    if not exists(join(config.base.path, config.base.config)):
        return config
    with open(join(config.base.path, config.base.config), 'r', encoding='utf-8') as file:
        config.set_from(load_toml(file))
    return config


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
    if ''.join(list1) != ''.join(list2):
        return False

    md5_1, md5_2 = "", ""
    for file in list1:
        with open(join(dir1, file), 'br') as f:
            md5_1 += str(md5(f.read()).hexdigest())
    for file in list2:
        with open(join(dir2, file), 'br') as f:
            md5_2 += str(md5(f.read()).hexdigest())
    return md5_1 == md5_2


def get_last_dir(dir: str, num: int = 0):
    if isdir(dir):
        dirs = [d for d in listdir(dir) if isdir(join(dir, d))]
        dirs.sort(key=lambda fn: getmtime(dir + "\\" + fn), reverse=True)
        if len(dirs) > num:
            return join(dir, dirs[num])
        else:
            return ""
    else:
        return ""


def backup_save_files(config: GameConfig, test: bool = False):
    """根据配置备份存档文件"""
    if platform[:3] != config.game.platform[:3]:
        print(f"Not same platform, skip {config.game.name}!")
        return -1
    backup_time = strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = join(config.base.path, backup_time)
    last_backup_dir = get_last_dir(config.base.path)
    if config.game.save_latest:
        save_path = get_last_dir(config.game.save_path)
    else:
        save_path = config.game.save_path
    if last_backup_dir != "" and is_same(save_path, last_backup_dir):
        print(f"Same saves, skip {config.game.name}!\n")
    else:
        if test:
            print(
                f"!!! Backup {config.game.name} test !!!\n" +
                f"    {save_path}\n" +
                f" -> {backup_dir}\n"
            )
            return 0

        copytree(save_path, backup_dir)
        print(
            f"Backup {config.game.name} successful:\n" +
            f"    {save_path}\n" +
            f" -> {backup_dir}\n"
        )


def init():
    if not isdir(backup_folder):
        makedirs(backup_folder)
    pass


def main():
    for folder in listdir(backup_folder):
        if isfile(join(backup_folder, folder, "config.toml")):
            config = load_config(folder)
            if config.check():
                backup_save_files(config=config, test=DEBUG)
            else:
                print(folder, config)


if __name__ == "__main__":
    init()
    main()
