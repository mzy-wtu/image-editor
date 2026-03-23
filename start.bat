@echo off

REM Simple Image Editor System Start Script

cls
echo Image Editor System
 echo ===================
echo Starting system...
echo.

REM Check if we're in the correct directory
echo Current directory: %cd%
echo.

REM Check if required directories exist
if not exist "frontend" (
    echo Error: Frontend directory not found
    echo Please make sure you are in the correct directory
    echo Press any key to exit...
    pause
    exit /b 1
)

if not exist "venv" (
    echo Error: Virtual environment not found
    echo Please create virtual environment first
    echo Press any key to exit...
    pause
    exit /b 1
)

REM Initialize database
echo Initializing database...
echo 1. Creating database if not exists...
venv\Scripts\python.exe app\db\create_db.py
echo.
echo 2. Initializing database tables...
venv\Scripts\python.exe app\db\init_db.py
echo.

REM Try to start backend directly
echo Starting Flask backend...
start "Flask Backend" cmd /k "venv\Scripts\python.exe -m flask run --host=localhost"
echo Backend started in new window
echo.

REM Try to start frontend development server directly
echo Starting Vue frontend development server...
start "Vue Frontend" cmd /k "cd frontend && npm run dev"
echo Frontend started in new window
echo.

REM Display success message
echo System started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause
