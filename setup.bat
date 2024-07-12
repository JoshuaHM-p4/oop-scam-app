@echo off

REM FRONT END SETUP
cd frontend
if not exist venv\Scripts\activate (
    python -m venv venv
    echo Created new virtual environment for frontend.
) else (
    echo Virtual environment for frontend already exists. You can now run front end venv locally.
)

echo Installing frontend dependencies...

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages if necessary
pip install -r requirements.txt

REM Deactivate virtual environment if activated
call venv\Scripts\deactivate.bat

echo Frontend setup completed.

cd ..

REM BACKEND SETUP

REM Check if venv exists, if not create it
cd backend
if not exist venv\Scripts\activate (
    python -m venv venv
    echo Created new virtual environment for backend.
) else (
    echo Virtual environment for backend already exists. You can now run front end venv locally.
)

echo Installing backend dependencies...

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages if necessary
pip install -r requirements.txt

echo Backend setup completed.

echo Setting up database...

REM Check if instance folder exists, if not create it
if not exist instance (
    mkdir instance
    echo Created instance folder.
)

REM Check if .flaskenv already exists
if exist .flaskenv (
    echo .flaskenv already exists.
) else (
    REM Create .flaskenv and add content
    echo FLASK_APP=run.py > .flaskenv
    echo FLASK_ENV=development >> .flaskenv
    echo .flaskenv file created.
)

REM Check if site.db exists
if not exist instance\site.db (
    echo site.db does not exist. Running migrations...
    call venv\Scripts\activate
    flask db upgrade
    echo Database setup completed.
) else (
    echo site.db already exists. No need to run migrations.
)

echo Backend setup completed.

REM Deactivate virtual environment if activated
call venv\Scripts\deactivate.bat

REM Pause to keep the window open and show messages
pause