@echo off

REM Image Editor System Stop Script

cls
echo ==================================
echo Image Editor System
 echo ==================================
echo Stopping system...
echo.

REM Stop all Python and npm processes
echo Stopping backend and frontend processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1

REM Display success message
echo ==================================
echo System stopped successfully!
echo ==================================
echo All processes have been terminated.
echo ==================================
echo Press any key to exit...
pause >nul
