@echo off
ECHO Starting the Python script from py_env...

:: Set the path to the virtual environment
SET VENV_PATH=D:\projects\py_env

:: Set the path to the Python script
SET PYTHON_SCRIPT=D:\projects\my_script.py

:: Activate the virtual environment
CALL %VENV_PATH%\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

:: Run the Python script
python %PYTHON_SCRIPT%
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python script failed to run.
    pause
    exit /b %ERRORLEVEL%
)

:: Deactivate the virtual environment
CALL deactivate
ECHO Script execution completed.
pause
