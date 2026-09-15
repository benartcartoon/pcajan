@echo off
setlocal
cd /d "%~dp0"
echo [1/5] Python paketleri kuruluyor...
python -m pip install --user pyautogui
if errorlevel 1 goto :err

echo [2/5] AI-Agent Drive klasorleri hazirlaniyor...
rclone mkdir gdrive:AI-Agent/jobs
rclone mkdir gdrive:AI-Agent/status
rclone mkdir gdrive:AI-Agent/logs
rclone mkdir gdrive:AI-Agent/results
if errorlevel 1 goto :err

echo [3/5] Yerel klasor hazirlaniyor...
if not exist "%USERPROFILE%\AI-Agent" mkdir "%USERPROFILE%\AI-Agent"

> "%~dp0start_agent.bat" echo @echo off
>> "%~dp0start_agent.bat" echo cd /d "%%~dp0"
>> "%~dp0start_agent.bat" echo python agent.py

> "%~dp0stop_agent.bat" echo @echo off
>> "%~dp0stop_agent.bat" echo taskkill /FI "WINDOWTITLE eq Komut Istemi - python agent.py" /F ^>nul 2^>^&1

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /Y "%~dp0start_agent.bat" "%STARTUP%\AI-Agent-Start.bat" >nul

echo [4/5] Windows otomatik baslatma ayarlandi.
echo [5/5] Google Drive baglantisi test ediliyor...
rclone lsd gdrive:AI-Agent

echo.
echo ========================================
echo TAMAMLANDI - PC AJAN v0.2 hazir.
echo Windows acilisinda otomatik baslayacak.
echo ========================================
pause
exit /b 0

:err
echo.
echo HATA: Kurulum tamamlanamadi.
pause
exit /b 1
