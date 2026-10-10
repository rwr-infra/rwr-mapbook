@echo off
rem NOTE: keep this file ASCII-only. cmd.exe parses .bat files with the console
rem code page, so non-ASCII lines next to "chcp 65001" get shredded into bogus
rem commands ("'ER' is not recognized as ..."). English comments only.

chcp 65001 >nul
title rwr-mapbook preview
cd /d "%~dp0"

rem Python: RWR_PYTHON (if set) > the portable one in this workspace (if present)
rem > python on PATH. serve.py probes for one that really has zensical+yaml+zhconv.
set "PY=%RWR_PYTHON%"
if not defined PY if exist "%~dp0..\..\..\_py\py314\python.exe" set "PY=%~dp0..\..\..\_py\py314\python.exe"
if not defined PY set "PY=python"

echo ============================================================
echo  rwr-mapbook  local preview  (hot reload)
echo  Open http://127.0.0.1:8000/ in your browser.
echo  First build takes a few seconds - please wait.
echo  Then every save shows up in about a second.
echo  Press Ctrl-C or close this window to stop.
echo ============================================================
echo.

"%PY%" "%~dp0serve.py" %*

echo.
echo Preview stopped.
pause
