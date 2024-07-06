@echo off

REM Open terminal 1 (Frontend)
start cmd /k "cd frontend & call venv\Scripts\activate & python src\main.py"

REM Open terminal 2 (Backend)
start cmd /k "cd backend & call venv\Scripts\activate & flask run"