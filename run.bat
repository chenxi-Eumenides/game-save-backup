@echo off

uv run main.py

for /f %%a in ('git status --porcelain ^| find /c "saves"') do set modified=%%a

if "%modified%"=="0" (
    echo 本地存档没有修改。
    pause
) else (
    :: 本地仓库有更新
    echo 更新了 %modified% 个存档文件
    git add saves
    git commit -m "更新游戏存档"
    git push
    pause
)
