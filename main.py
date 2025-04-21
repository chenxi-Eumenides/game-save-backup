#!/bin/python

from toml import load as load_toml

from os.path import exists, isdir, isfile, join
from os import listdir, makedirs
from shutil import copytree
from time import strftime

# define
backup_folder = "saves"


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


def load_config(game: str = "none"):
    """
    加载并解析 TOML 配置文件\n
    game: 游戏名称，与文件夹名保持一致
    """
    config = GameConfig()
    config.base.path = join(backup_folder, game)
    if not exists(join(config.base.path, config.base.config)):
        return config
    with open(join(config.base.path, config.base.config), 'r', encoding='utf-8') as file:
        config.set_from(load_toml(file))
    return config


def backup_save_files(config: GameConfig):
    """根据配置备份存档文件"""
    # 创建备份目录

    backup_time = strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = join(config.base.path, backup_time)
    copytree(config.game.save_path, backup_dir)

    # makedirs(backup_dir, exist_ok=True)
    # for save_path in listdir(config.game.save_path):
    #     full_save_path = join(config.game.save_path, save_path)
    #     if isfile(full_save_path):
    #         # 如果是文件，直接复制
    #         copy(full_save_path, backup_dir)
    #     elif isdir(full_save_path):
    #         # 如果是文件夹，复制整个文件夹
    #         copytree(full_save_path, backup_dir)
    #     print(f"Backup successful: {full_save_path} -> {game_backup_dir}")

    print(
        f"Backup {config.game.name} successful:\n" +
        f"    {config.game.save_path}\n" +
        f" -> {backup_dir}")


def init():
    if not isdir(backup_folder):
        makedirs(backup_folder)
    pass


def main():
    for folder in listdir(backup_folder):
        if isfile(join(backup_folder, folder, "config.toml")):
            config = load_config(folder)
            if config.check():
                backup_save_files(config=config)
            else:
                print(folder, config)


if __name__ == "__main__":
    init()
    main()
