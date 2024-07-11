@echo off

REM Open terminal 2 (Backend)
start cmd /k "cd backend & call venv\Scripts\activate & flask run"