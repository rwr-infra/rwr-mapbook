@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title stop preview
cd /d "%~dp0"

rem NOTE: keep this file ASCII-only. cmd.exe parses .bat files with the console
rem code page, and non-ASCII lines next to "chcp 65001" get shredded into
rem bogus commands ("'ER' is not recognized as ..."). English comments only.

set PORT=8000
if not "%~1"=="" set PORT=%~1
set /a BUILDER=%PORT%+1000

echo ============================================================
echo  Stop the preview that is listening on port %PORT%
echo  (and its builder on port %BUILDER%, if any)
echo  Usage:  stop.bat          (port 8000)
echo          stop.bat 8010     (another port)
echo ============================================================
echo.

for %%P in (%PORT% %BUILDER%) do call :kill %%P

echo.
echo Done.
pause
exit /b 0

:kill
set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr LISTENING ^| findstr ":%~1"') do (
  set FOUND=1
  set "IMG="
  for /f "tokens=1" %%b in ('tasklist /FI "PID eq %%a" /FO CSV /NH 2^>nul') do set "IMG=%%~b"
  echo Found PID %%a on port %~1 : !IMG!
  rem Only kill python (the preview and its builder are python). If the image
  rem name says it is something else, leave it alone. If we could not get a
  rem name at all, fall back to the old behaviour (just kill it).
  if defined IMG (
    echo !IMG! | findstr /I "python" >nul
    if errorlevel 1 (
      echo   !IMG! is not python - leaving it alone.
    ) else (
      echo Stopping it...
      taskkill /PID %%a /F
    )
  ) else (
    echo Stopping it...
    taskkill /PID %%a /F
  )
  echo.
)
if "%FOUND%"=="0" (
  echo Nothing is listening on port %~1 - already stopped.
)
exit /b 0
