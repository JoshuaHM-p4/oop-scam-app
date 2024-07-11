@echo off

REM Open terminal 1 (Frontend)
start cmd /k "cd frontend & call venv\Scripts\activate & python src\main.py"