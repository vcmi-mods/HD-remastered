@echo off
setlocal enabledelayedexpansion

rem === Configuration ===
set "ORG=C:\Users\Administrator\Documents\My Games\vcmi\Mods\_HDModtest\ORG"
set "ERAHD=C:\Users\Administrator\Documents\My Games\vcmi\Mods\_HDModtest\ERAHD"
set "SCRIPT=C:\Users\Administrator\Documents\My Games\vcmi\Mods\_HDModtest\def2json.py"

rem === Run def2json.py for each .def file in ORG folder ===
echo [INFO] Running def2json.py on DEF files in: %ORG%
for %%F in ("%ORG%\*.def") do (
    echo [INFO] Processing %%~nxF ...
    python "%SCRIPT%" --hdremaster "%%F"
	del /q "%%F" >nul
	
	for %%G in ("%ORG%\%%~nF\*shadow*") do (
		del /q "%%G" >nul
	)
	
	for %%G in ("%ORG%\%%~nF\*overlay*") do (
		del /q "%%G" >nul
	)
	
)

rem === Rename ERAHD subfolders that end with ".def" ===
echo [INFO] Renaming ERAHD folders that end with ".def" in: %ERAHD%
for /d %%D in ("%ERAHD%\*.def") do (
    set "old=%%~nxD"
    set "new=!old:.def=!"
    echo [INFO] Renaming "%%~fD" to "!new!"
    ren "%%~fD" "!new!"
	
	for %%F in ("%ORG%\!new!\*.txt") do (
		del /q "%%G" >nul
	)
)

echo [DONE] All operations completed.
pause
