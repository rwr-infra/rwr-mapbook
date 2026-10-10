@echo off
rem NOTE: keep this file ASCII-only. cmd.exe parses .bat files with the console
rem code page, so non-ASCII lines next to "chcp 65001" get shredded into bogus
rem commands. English comments only.

chcp 65001 >nul
cd /d "%~dp0"

rem Python: RWR_PYTHON (if set) > the portable one in this workspace (if present)
rem > python on PATH. Anything with boto3 installed will do.
set "PY=%RWR_PYTHON%"
if not defined PY if exist "%~dp0..\..\..\_py\py314\python.exe" set "PY=%~dp0..\..\..\_py\py314\python.exe"
if not defined PY set "PY=python"

"%PY%" "%~dp0r2.py" %*

if errorlevel 1 (
  echo.
  echo The command ended with a non-zero exit code - see the lines above.
  echo ^(for "verify" that means it found something to look at^)
  pause
)
