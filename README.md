# game-save-backup
this is my game saves backup

## file tree

```bash
.
├─main.py
└─saves
  ├─game-1
  │ ├─game-1.toml # backup setting config
  │ ├─time-1
  │ │ └─save-file-1
  │ └─time-2
  │   └─save-file-2
  └─game-2
    ├─game-2.toml
    └─time-3
      └─save-file-3
```

## config

{any name}.toml

```toml
[game]
name = "template" # 游戏名称
name-zh-cn = "模板" # 游戏名称中文
platform = "win10" # 运行平台：win10 linux mac android ios win7 winxp ns
path = 'C:\Games' # 游戏路径
exe_path = 'C:\Games\template.exe' # 运行文件相对路径
save_path = 'C:\Games\template\saves' # 存档文件相对路径，可以是文件夹或单文件
save_latest = false # 是否只保存save_path下最新创建的文件夹，用于游戏存档只增不减的情况
is_folder = true # 目标是否是文件夹，不然是单文件，只在save_latest为true时生效
need_zip = false # 是否需要压缩 (未完成该功能)

[base]
download = "steam" # steam，或下载地址/页面

```

you can create multiple config files if you need backup diffent saves for one game.