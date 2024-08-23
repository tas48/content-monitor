@echo off
cd C:\work_dir\content-monitor
call venv\Scripts\activate  (se estiver usando um ambiente virtual)
fastapi dev main.py
