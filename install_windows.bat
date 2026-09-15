@echo off
setlocal
cd /d %USERPROFILE%

where git >nul 2>nul
if errorlevel 1 (
  echo HATA: Git bulunamadi.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo HATA: Python bulunamadi.
  pause
  exit /b 1
)

if not exist "%USERPROFILE%\pcajan" (
  git clone https://github.com/benartcartoon/pcajan.git "%USERPROFILE%\pcajan"
) else (
  cd /d "%USERPROFILE%\pcajan"
  git pull
)

cd /d "%USERPROFILE%\pcajan"

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
(
 echo @echo off
 echo cd /d "%USERPROFILE%\pcajan"
 echo python agent.py
) > "%STARTUP%\PCAjan.bat"

echo.
echo PC AJAN KURULDU.
echo Windows acilisinda otomatik baslayacak.
echo Simdi test icin agent baslatiliyor...
echo.
python agent.py
