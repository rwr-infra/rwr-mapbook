@echo off
rem NOTE: keep this file ASCII-only (see start.bat for why).

chcp 65001 >nul
cd /d "%~dp0"

rem Python: RWR_PYTHON (if set) > the portable one in this workspace (if present)
rem > python on PATH.
set "PY=%RWR_PYTHON%"
if not defined PY if exist "%~dp0..\..\..\_py\py314\python.exe" set "PY=%~dp0..\..\..\_py\py314\python.exe"
if not defined PY set "PY=python"

"%PY%" "%~dp0fullcheck.py"

echo.
echo Done - see the summary above.
pause
