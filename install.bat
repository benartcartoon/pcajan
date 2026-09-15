@echo off
setlocal
cd /d "%~dp0"
echo [1/4] AI-Agent Drive klasorleri hazirlaniyor...
rclone mkdir gdrive:AI-Agent/jobs
rclone mkdir gdrive:AI-Agent/status
rclone mkdir gdrive:AI-Agent/logs
if errorlevel 1 goto :err

echo [2/4] Yerel klasor hazirlaniyor...
if not exist C:\AI-Agent mkdir C:\AI-Agent

> "%~dp0start_agent.bat" echo @echo off
>> "%~dp0start_agent.bat" echo if not exist C:\AI-Agent mkdir C:\AI-Agent
>> "%~dp0start_agent.bat" echo start "AI-Agent Drive" /min rclone mount gdrive:AI-Agent C:\AI-Agent --vfs-cache-mode writes --dir-cache-time 30s --poll-interval 15s

> "%~dp0stop_agent.bat" echo @echo off
>> "%~dp0stop_agent.bat" echo taskkill /IM rclone.exe /F ^>nul 2^>^&1

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /Y "%~dp0start_agent.bat" "%STARTUP%\AI-Agent-Start.bat" >nul

echo [3/4] Windows otomatik baslatma ayarlandi.
call "%~dp0start_agent.bat"
timeout /t 4 /nobreak >nul

echo [4/4] Baglanti test ediliyor...
dir C:\AI-Agent

echo.
echo ========================================
echo TAMAMLANDI - AI-Agent artik Windows acilisinda otomatik baslayacak.
echo ========================================
pause
exit /b 0

:err
echo.
echo HATA: Google Drive baglantisi kurulurken sorun olustu.
echo Once su komutu test et: rclone lsd gdrive:
pause
exit /b 1
