@echo off
setlocal enabledelayedexpansion

rem === Paths ===
set "SPRITES=C:\Users\Administrator\Documents\My Games\vcmi\Mods\hd-remaster\content\sprites"
set "ORG=C:\Users\Administrator\Documents\My Games\vcmi\Mods\_HDModtest\ORG"

echo [INFO] Copying JSON files to sprite folders...

for /d %%D in ("%SPRITES%\*") do (
    set "foldername=%%~nxD"
    set "jsonsource=%ORG%\!foldername!.json"
    set "target=%%~fD"

    if exist "!jsonsource!" (
        echo [OK] Copying !jsonsource! to !target!
        copy /Y "!jsonsource!" "!target!\"
		del /q "!jsonsource!" >nul
		rd /q "%ORG%\!foldername!" >nul
    ) else (
        echo [WARN] JSON not found for !foldername!
    )
)

echo [DONE] All matching JSON files processed.
pause
