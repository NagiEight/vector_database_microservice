@echo off
title Vector DB Microservice Launcher

REM Navigate to the directory containing the bat file
cd /d "%~dp0"

echo.
echo ====================================================================
echo == Starting the Vector Database Microservice                      ==
echo ====================================================================
echo.

REM Check for Python installation and install dependencies if needed
echo Checking for Python and installing dependencies...
python -c "import sys; print(sys.executable)" > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python (and make sure to add it to your PATH).
    echo.
    pause
    exit /b 1
)

pip install -r requirements.txt
echo Dependencies installed successfully.
echo.

REM Start the FastAPI backend in a new command prompt window
echo Starting FastAPI Backend...
start cmd /k "python main.py"

timeout /t 5 > nul

REM Start the Python web GUI in a new command prompt window
echo Starting Web GUI Frontend...
start cmd /k "cd webgui && python server.py"

echo.
echo ====================================================================
echo == HELP MENU                                                      ==
echo ====================================================================
echo.
echo The services are now running in the background.
echo.
echo 1. Access the Web GUI:
echo    Open your web browser and go to:
echo    http://localhost:8080
echo.
echo 2. Interact via cURL (for developers):
echo.
echo    Example: Add new vectors
echo    ^>^> curl -X POST http://localhost:8000/vectors/add -H "Content-Type: application/json" -d "{
echo    "texts": [ "A cat is a type of feline.", "The sun is the star at the center of the Solar System." ],
echo    "metadata": [ { "animal_type": "mammal" }, { "celestial_body": "star" } ]
echo    }"
echo.
echo    Example: Search for similar vectors
echo    ^>^> curl -X POST http://localhost:8000/vectors/search -H "Content-Type: application/json" -d "{
echo    "query": "What is the largest celestial body?",
echo    "k": 2
echo    }"
echo.
echo Press any key to exit this window...
pause > nul
exit