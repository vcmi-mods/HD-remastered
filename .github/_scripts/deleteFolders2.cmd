@echo off
setlocal enabledelayedexpansion

rem === Path to sprites folder ===
set "SPRITES=C:\Users\Administrator\Documents\My Games\vcmi\Mods\hd-remaster\content\sprites"

echo [INFO] Cleaning up folders without matching .json...

for /d %%D in ("%SPRITES%\*") do (
    set "foldername=%%~nxD"
    set "jsonfile=%SPRITES%\!foldername!.json"

    if not exist "!jsonfile!" (
        echo [DELETE] No .json for !foldername!  deleting folder %%~fD
        rmdir /s /q "%%~fD"
    ) else (
        echo [OK] JSON exists for !foldername!
    )
)

echo [DONE] Orphan folders removed.
pause
