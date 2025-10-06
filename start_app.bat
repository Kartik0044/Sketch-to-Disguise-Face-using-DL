@echo off
echo Starting Sketch2Face Web Application...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
    echo.
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask, torch, torchvision, PIL" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Flask application...
echo Open your web browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server.
echo.

python app.py

pause