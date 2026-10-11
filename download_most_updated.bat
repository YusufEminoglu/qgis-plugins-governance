@echo off
chcp 65001 >nul
title QGIS Plugins Downloader - Latest Versions

echo =========================================================
echo  QGIS Plugins Downloader (Most Updated Only)
echo  Author: Yusuf Eminoglu
echo =========================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0download_most_updated.ps1" %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [BILGI] Indirme islemi basariyla tamamlandi.
    echo.
    echo Devam etmek icin bir tusa basin...
    pause >nul
    exit /b 0
) else (
    echo.
    echo [HATA] Indirme islemi sirasinda bir sorun olustu.
    pause
    exit /b 1
)
