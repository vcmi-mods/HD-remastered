@echo off
setlocal enabledelayedexpansion

rem === Path to sprites folder ===
set "SPRITES=C:\Users\Administrator\Documents\My Games\vcmi\Mods\hd-remaster\content\sprites"

echo [INFO] Cleaning up orphan .json files...

for %%F in ("%SPRITES%\*.json") do (
    set "jsonfile=%%~nxF"
    set "basename=%%~nF"
    set "folderpath=%SPRITES%\!basename!"

    if not exist "!folderpath!\" (
        echo [DELETE] No folder for !basename! deleting %%~fF
        del "%%~fF"
    ) else (
        echo [OK] Folder exists for !basename!
    )
)

echo [DONE] Orphan JSON files removed.
pause
