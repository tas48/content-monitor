@echo off
call python3 -m venv venv
call venv\Scripts\activate  
fastapi dev main.py
