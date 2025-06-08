#!/bin/python

# system lib
from hashlib import md5
from os import listdir, makedirs
from os.path import basename, exists, getctime, isdir, isfile, join
from shutil import copy2, copytree
from sys import argv, platform
from time import strftime

# third part lib
from toml import load as load_toml

# define
backup_folder = "saves"
max_file = 1024 * 1024 * 10
output_level = 0
DEBUG = False


class GameConfig:
    """
    游戏配置类
    """

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
        is_folder: bool = True
        need_zip: bool = False

    def __init__(self, folder_name: str = "none", config_file: str = "config.toml"):
        self.output_level = output_level
        self.base = self.__config_base()
        self.game = self.__config_game()
        self.load_config(folder_name, config_file)
        self.status = self.check()
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
            + f"        need_zip:  {self.game.need_zip}\n"
            + "    }\n"
            + "    base: {\n"
            + f"        path:      {self.base.path}\n"
            + f"        config:    {self.base.config}\n"
            + f"        download:  {self.base.download}\n"
            + "    }\n"
            + "}"
        )

    def set_from(self, data: dict):
        game: dict = data.get("game")
        base: dict = data.get("base")
        if game is None or base is None:
            raise "data is wrong"
        self.game.name = d if (d := game.get("name")) is not None else self.__config_game.name
        self.game.name_zh_cn = d if (d := game.get("name-zh-cn")) is not None else self.__config_game.name_zh_cn
        self.game.platform = d if (d := game.get("platform")) is not None else self.__config_game.platform
        self.game.path = d if (d := game.get("path")) is not None else self.__config_game.path
        self.game.exe_path = d if (d := game.get("exe_path")) is not None else self.__config_game.exe_path
        self.game.save_path = d if (d := game.get("save_path")) is not None else self.__config_game.save_path
        self.game.save_latest = d if (d := game.get("save_latest")) is not None else self.__config_game.save_latest
        self.game.is_folder = d if (d := game.get("is_folder")) is not None else self.__config_game.is_folder
        self.game.need_zip = d if (d := game.get("need_zip")) is not None else self.__config_game.need_zip
        self.base.download = d if (d := base.get("download")) is not None else self.__config_base.download

    def check(self) -> bool:
        # must have
        if not self.game.name:
            if 1 <= self.output_level <= 5:
                print(f"[ERROR] not game name in {join(self.base.path, self.base.config)}")
            return False
        if not self.game.save_path:
            if 1 <= self.output_level <= 5:
                print(f"[ERROR] not game save path in {self.game.name}")
            return False
        if not self.base.path or not isdir(self.base.path):
            if 1 <= self.output_level <= 5:
                print(f"[ERROR] not base path in {self.game.name}")
            return False
        # not must have
        if not self.game.name_zh_cn:
            if 2 <= self.output_level <= 5:
                print(f"[WRONG] not game name zh-cn in {join(self.base.path, self.base.config)}")
        if not self.game.platform:
            if 2 <= self.output_level <= 5:
                print(f"[WRONG] not game platform in {self.game.name}")
        if not self.game.path or not isdir(self.game.path):
            if 2 <= self.output_level <= 5:
                print(f"[WRONG] not game path in {self.game.name}")
        if not self.game.exe_path or not isfile(self.game.exe_path):
            if 2 <= self.output_level <= 5:
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


def get_all_file(orgin: str, file_list: list[str] = None, dir: str = "") -> list[str]:
    """
    递归获取所有文件夹

    :param orgin: 最外层文件夹路径
    :param file_list: 返回的文件夹路径列表, defaults to None
    :param dir: 下一个要获取的子文件夹名, defaults to ""
    :return: 所有文件名的列表
    """
    if file_list is None:
        file_list = []
    if isfile(join(orgin, dir)):
        file_list.append(dir)
    elif isdir(join(orgin, dir)):
        for f in listdir(join(orgin, dir)):
            get_all_file(orgin, file_list, join(dir, f))
    return file_list


def is_same(dir1: str, dir2: str, is_folder: bool = True) -> bool:
    """
    计算所有文件的md5，判断文件夹是否一致

    :param dir1: 文件夹1路径
    :param dir2: 文件夹2路径
    :param is_folder: 是否是文件夹，不是需要将文件夹1的最后一个添加到文件夹2路径中, defaults to True
    :return: 是或否
    """
    if not is_folder:
        dir2 = join(dir2, basename(dir1))
    list1 = get_all_file(dir1)
    list2 = get_all_file(dir2)
    if len(list1) != len(list2):
        return False
    if "".join(list1) != "".join(list2):
        return False

    # 计算所有文件的md5，相加判断是否一致。
    md5_1, md5_2 = [], []
    for file in list1:
        with open(join(dir1, file), "br") as f:
            md5_1.append(str(md5(f.read()).hexdigest()))
    for file in list2:
        with open(join(dir2, file), "br") as f:
            md5_2.append(str(md5(f.read()).hexdigest()))
    return md5_1 == md5_2


def copy(src: str, tgt: str, is_folder: bool = True):
    """
    复制文件或文件夹

    :param src: 源文件夹
    :param tgt: 目标文件夹
    :param is_folder: 要复制的是否是文件夹，如果不是，则需要先创建目标文件夹, defaults to True
    """
    if is_folder:
        copytree(src, tgt)
    else:
        makedirs(tgt)
        copy2(src, tgt)


def is_toml(src: str):
    """
    判断是否是toml文件

    :param src: 文件路径
    :return: 是或否
    """
    if len(src) <= 5:
        return False
    return src[-5:] == ".toml"


def get_last(dir: str, is_folder: bool = True, num: int = 0):
    """获取文件夹下最新的文件或文件夹

    Args:
        dir (str): 寻找的文件夹路径
        is_folder (bool, optional): 要寻找的是否是文件夹. Defaults to True.
        num (int, optional): 排序的第几个. Defaults to 0.

    Returns:
        str: 文件或文件夹路径
    """
    if isdir(dir):
        # 获取所有符合要求的文件名列表
        if is_folder:
            items = [i for i in listdir(dir) if isdir(join(dir, i))]
        else:
            items = [i for i in listdir(dir) if isfile(join(dir, i))]
        # 逆向排序(从新到老)
        items.sort(key=lambda fn: getctime(dir + "\\" + fn), reverse=True)
        # 返回第一个
        if len(items) > num:
            return join(dir, items[num])
        else:
            return ""
    else:
        return ""


def is_support_platform(game_platform: str):
    """
    是否是支持的平台

    game_platform: win10 linux mac android ios win7 winxp ns
    """
    if platform[:3] == game_platform[:3]:
        return True
    # ns手动备份至win
    if platform[:3] == "win" and game_platform in ["win10", "ns"]:
        return True
    return False


def backup_save_files(config: GameConfig, need_folder: bool = False):
    """
    根据配置备份存档文件
    """
    global DEBUG
    if not is_support_platform(config.game.platform):
        print(f"Not support platform, skip {config.game.name}!")
        return -1
    backup_time = strftime("%Y-%m-%d_%H-%M-%S")

    if config.game.save_latest:
        # 最新的
        save_path = get_last(config.game.save_path, config.game.is_folder)
    else:
        # 全部
        save_path = config.game.save_path
    if need_folder:
        # 需多层
        backup_dir = join(config.base.path, backup_time, basename(save_path))
        latest_backup = join(get_last(config.base.path, True), basename(save_path))
    else:
        # 无需多层
        backup_dir = join(config.base.path, backup_time)
        latest_backup = get_last(config.base.path, True)

    if latest_backup != "" and is_same(save_path, latest_backup, config.game.is_folder):
        # 有过备份，且最新备份相同
        print(f"[INFO] {config.game.name_zh_cn} ({config.base.config}) same saves, skip !")
    else:
        # 开始备份
        print(f"[INFO] {config.game.name_zh_cn} backup :\n" + f"    {save_path}\n" + f" -> {backup_dir}")
        if not DEBUG:
            copy(save_path, backup_dir, config.game.is_folder)
            print(f"[INFO] Success!\n")


def init():
    """
    检查saves文件夹是否创建
    """
    if not isdir(backup_folder):
        makedirs(backup_folder)


def main(args):
    """
    挨个备份
    """
    # 检查指定的游戏是否存在
    target_games = []
    for arg in args:
        if arg in listdir(backup_folder):
            target_games.append(arg)
    # 获取所有的备份文件夹
    for folder in listdir(backup_folder):
        if isfile(join(backup_folder, folder)):
            continue
        # 指定了游戏，则仅在匹配时备份
        if len(target_games) > 0 and folder not in target_games:
            continue
        # 列出文件夹下的所有配置文件
        files = [f for f in listdir(join(backup_folder, folder)) if is_toml(join(backup_folder, folder, f))]
        for file in files:
            if isfile(join(backup_folder, folder, file)):
                # 检查配置并备份
                config = GameConfig(folder, file)
                if config.status:
                    backup_save_files(config=config, need_folder=len(files) > 1)


if __name__ == "__main__":
    init()
    main(argv)
