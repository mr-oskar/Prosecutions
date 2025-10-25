@echo off
echo =========================================
echo   System Guardian - Starting Services
echo =========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python 3.11 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python found: %PYTHON_VERSION%
echo.

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q

echo.
echo Creating required directories...
if not exist "db" mkdir db
if not exist "reports\pdfs" mkdir reports\pdfs
if not exist "reports\json" mkdir reports\json

echo.
echo =========================================
echo   Starting Servers
echo =========================================
echo.
echo Backend will run on: http://localhost:8000
echo Web Interface will run on: http://localhost:5000
echo.

echo Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo Starting Flask Web Interface...
start "Flask Web Interface" cmd /k "venv\Scripts\activate.bat && python ui\app.py"

echo.
echo =========================================
echo   Both servers are running!
echo =========================================
echo.
echo   Web Interface: http://localhost:5000
echo   Admin Panel:   http://localhost:5000/admin
echo   API Docs:      http://localhost:8000/docs
echo.
echo Close the server windows to stop the application.
echo =========================================
echo.
pause
