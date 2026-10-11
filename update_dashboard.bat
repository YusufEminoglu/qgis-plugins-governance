@echo off
chcp 65001 >nul
title QGIS Plugins Analytics Dashboard Updater

echo ==========================================================
echo  QGIS Plugin Analytics ^& Governance Dashboard Updater
echo ==========================================================
echo.

cd /d "%~dp0"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0update_dashboard.ps1"

if %ERRORLEVEL% equ 0 (
    echo.
    echo [BILGI] Dashboard guncellemesi basariyla tamamlandi.
    echo Tarayicida aciliyor...
    start "" "%USERPROFILE%\Downloads\qgis_plugins_dashboard.html"
) else (
    echo.
    echo [HATA] Guncelleme sirasinda bir sorun olustu. Hata kodu: %ERRORLEVEL%
)

echo.
echo Devam etmek icin bir tusa basin...
pause >nul
