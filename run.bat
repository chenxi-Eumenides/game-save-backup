@echo off

echo 开始备份存档：

echo ↓
uv run main.py
echo ↑

echo 开始检查存档更新：

echo ↓
for /f %%a in ('git status --porcelain ^| findstr "saves" ^| find /c /v ""') do set modified=%%a
echo ↑

if "%modified%"=="0" (
    echo 本地存档没有修改。
    pause
) else (
    echo 更新了 %modified% 个存档文件。

    echo ↓
    git add saves
    git commit -m "更新游戏存档 by 懒人脚本"
    echo ↑

    echo 推送至github仓库

    echo ↓
    git push
    echo ↑

    echo 存档已完成备份
    pause
)
